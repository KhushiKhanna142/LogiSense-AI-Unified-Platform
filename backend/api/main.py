import asyncio
from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from agents.observer.agent import run_observer
from agents.reasoner.agent import run_reasoner
from agents.actor.agent import run_actor
from api.websocket import ws_manager
from db.supabase_client import get_active_shipments

app = FastAPI(title='LogiSense AI', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],   # tighten in production
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def startup():
    """Start Observer Agent when FastAPI starts."""
    asyncio.create_task(run_observer())
    asyncio.create_task(run_reasoner())
    asyncio.create_task(run_actor())
    print('Observer + Reasoner + Actor Agents started.')


@app.websocket('/ws/anomalies')
async def websocket_endpoint(websocket: WebSocket):
    """
    Dashboard connects here.
    Publisher (F1) broadcasts anomaly events here.
    """
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, wait for client messages if any
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


@app.get('/api/cascade/{incident_id}')
async def get_cascade_tree(incident_id: str):
    """Fetch a cached CascadeTree by incident_id."""
    from streams.redis_client import cache_get
    tree = cache_get(f'incident:{incident_id}')
    return tree or {'error': 'not found'}

@app.get('/api/shipments/active')
async def active_shipments():
    """REST endpoint — returns all active shipments for initial dashboard load."""
    return get_active_shipments()


@app.get('/api/health')
async def health():
    return {'status': 'ok', 'agent': 'Observer running'}


@app.post('/api/trigger-scan')
async def trigger_scan():
    """Immediately run one full Observer + Reasoner cycle. Used by demo_seed.py."""
    import asyncio
    from agents.observer.agent import poll_and_detect
    from agents.reasoner.agent import process_event_batch, ReasonerState
    
    # 1. Run Observer poll (sync, in thread pool to avoid blocking event loop)
    loop = asyncio.get_event_loop()
    cycle, anomalies = await loop.run_in_executor(None, poll_and_detect, 99)
    print(f'[trigger-scan] Observer: {len(anomalies)} anomalies queued')
    
    # 2. Broadcast anomalies to WebSocket immediately
    for ev in anomalies:
        await ws_manager.broadcast(ev)
    
    # 3. Run Reasoner cycle (sync)
    state = ReasonerState(cycle=0, events_processed=0, last_incident_id='')
    state = await loop.run_in_executor(None, process_event_batch, state)
    print(f'[trigger-scan] Reasoner processed {state["events_processed"]} events')
    
    return {'anomalies': len(anomalies), 'reasoner_events': state['events_processed']}

@app.get('/api/carriers/reliability')
async def carrier_reliability():
    """Return current reliability scores for all carriers."""
    from db.supabase_client import get_all_carriers
    carriers = get_all_carriers()
    return [
        {
            'carrier_id': cid,
            'reliability_score': c.get('current_reliability_score', 0),
            'blacklisted': c.get('blacklisted', False),
        }
        for cid, c in carriers.items()
    ]
 
@app.get('/api/decisions/recent')
async def recent_decisions():
    """Return last 20 decisions from decision_log for dashboard."""
    from db.supabase_client import get_client
    client = get_client()
    result = client.table('decision_log') \
        .select('decision_id, decision_type, agent, sha256_hash, created_at, payload') \
        .order('created_at', desc=True) \
        .limit(20) \
        .execute()
    return result.data or []


@app.get('/api/swaps/recent')
async def recent_swaps():
    """Return last 10 carrier swaps read from Redis swap cache."""
    from streams.redis_client import get_redis
    import json
    r = get_redis()
    if not r:
        return []
    keys = r.keys('swap:SWAP-*')
    swaps = []
    for key in keys:
        val = r.get(key)
        if val:
            try:
                swaps.append(json.loads(val))
            except Exception:
                pass
    # Sort newest first by timestamp
    swaps.sort(key=lambda s: s.get('timestamp', ''), reverse=True)
    return swaps[:10]

# ── F4 REST Endpoints ────────────────────────────────────────────
@app.get('/api/warehouses')
async def get_warehouses():
  """Returns all warehouse states for initial heatmap load."""
  from streams.redis_client import get_all_warehouse_loads
  from db.supabase_client import get_all_warehouses
  warehouses = get_all_warehouses()
  loads = get_all_warehouse_loads()
  # Merge Redis live loads into Supabase base data
  for wh in warehouses:
    live = loads.get(wh['warehouse_id'])
    if live: wh.update(live)
  return warehouses
