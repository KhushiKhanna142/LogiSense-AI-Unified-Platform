import { useState, useEffect } from 'react'
import AnomalyBadge from './components/AnomalyBadge'
import CascadeTree from './components/CascadeTree'
import SwapNotification from './components/SwapNotification'
import WarehouseHeatmap from './components/WarehouseHeatmap'
import ExplainabilityDashboard from './components/features/explainability/ExplainabilityDashboard'
import ZenPlatform from './components/zen/ZenPlatform'

function App() {
    const [activeTab, setActiveTab] = useState('LOGISENSE');
    const [explainabilityData, setExplainabilityData] = useState(null);

    const fetchExplainabilityData = () => {
        fetch('http://localhost:8000/api/explainability/demo_data')
            .then(res => res.json())
            .then(data => setExplainabilityData(data))
            .catch(err => console.error("Explainability Demo Load Error:", err));
    };

    useEffect(() => {
        fetchExplainabilityData();
    }, []);

    const renderTabs = () => {
        return (
            <>
                <div className={`w-full max-w-4xl space-y-6 ${activeTab !== 'LOGISENSE' ? 'hidden' : ''}`}>
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

                <div className={`w-full max-w-6xl text-white ${activeTab !== 'EXPLAINABILITY' ? 'hidden' : ''}`}>
                    {explainabilityData ? (
                        <ExplainabilityDashboard
                            predictions={explainabilityData.predictions}
                            features={explainabilityData.features}
                            modelKey={explainabilityData.modelKey}
                            onRegenerate={fetchExplainabilityData}
                        />
                    ) : (
                        <div className="text-center py-20 text-gray-400">Loading ML Explanation Models...</div>
                    )}
                </div>

                <div className={`w-full max-w-6xl h-[800px] bg-white rounded-xl overflow-hidden shadow-2xl border border-gray-700 ${activeTab !== 'ZEN' ? 'hidden' : ''}`}>
                    <ZenPlatform />
                </div>
            </>
        );
    };

    return (
        <div className="min-h-screen bg-gray-900 flex flex-col items-center py-10 w-full px-4">
            <div className="flex flex-col items-center mb-8">
                <h1 className="text-4xl font-bold text-white mb-2">LogiSense AI Unified Platform</h1>
                <p className="text-gray-400">Multi-Agent Intelligence & Autonomous Supply Chain Recovery</p>
            </div>

            {/* Navigation Tabs */}
            <div className="flex space-x-4 mb-8 bg-gray-800 p-2 rounded-lg border border-gray-700">
                <button
                    onClick={() => setActiveTab('LOGISENSE')}
                    className={`px-6 py-2 rounded-md font-medium transition-colors ${activeTab === 'LOGISENSE' ? 'bg-blue-600 text-white shadow-lg' : 'text-gray-400 hover:text-white hover:bg-gray-700'}`}
                >
                    LogiSense (F1-F4)
                </button>
                <button
                    onClick={() => setActiveTab('EXPLAINABILITY')}
                    className={`px-6 py-2 rounded-md font-medium transition-colors ${activeTab === 'EXPLAINABILITY' ? 'bg-purple-600 text-white shadow-lg' : 'text-gray-400 hover:text-white hover:bg-gray-700'}`}
                >
                    Agent Explainability (F8)
                </button>
                <button
                    onClick={() => setActiveTab('ZEN')}
                    className={`px-6 py-2 rounded-md font-medium transition-colors ${activeTab === 'ZEN' ? 'bg-emerald-600 text-white shadow-lg' : 'text-gray-400 hover:text-white hover:bg-gray-700'}`}
                >
                    Zen Platform (Dec / RTO / ETA)
                </button>
            </div>

            {renderTabs()}
        </div>
    )
}

export default App
