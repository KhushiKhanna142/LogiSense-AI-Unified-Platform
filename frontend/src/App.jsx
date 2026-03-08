import AnomalyBadge from './components/AnomalyBadge'
import CascadeTree from './components/CascadeTree'
import SwapNotification from './components/SwapNotification'
import WarehouseHeatmap from './components/WarehouseHeatmap'

function App() {
    return (
        <div className="min-h-screen bg-gray-900 flex flex-col items-center py-10">
            <h1 className="text-3xl font-bold mb-8 text-white">LogiSense AI: Observer, Reasoner, Actor</h1>

            <div className="w-full max-w-4xl space-y-6">
                {/* F2: Reasoner Agent Cascade Tree */}
                <div className="bg-gray-800 rounded-xl shadow-2xl border border-gray-700">
                    <CascadeTree />
                </div>

                {/* F1: Observer Agent Feed */}
                <div className="bg-gray-800 rounded-xl shadow-2xl border border-gray-700">
                    <AnomalyBadge />
                </div>

                {/* F3: Actor Agent Swap Notifications */}
                <div className="bg-gray-800 rounded-xl shadow-2xl border border-gray-700">
                    <SwapNotification />
                </div>

                {/* F4: Warehouse Congestion Heatmap */}
                <div className="bg-gray-800 rounded-xl overflow-hidden shadow-2xl border border-gray-700">
                    <WarehouseHeatmap />
                </div>
            </div>
        </div>
    )
}

export default App
