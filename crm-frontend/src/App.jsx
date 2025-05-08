import React, { useState } from "react";
import CarList from "./components/CarList";
import PartList from "./components/PartList";
import RepairList from "./components/RepairList";
import BudgetView from "./components/BudgetView";
import Sidebar from "./components/Sidebar";

export default function App() {
  const [activeMenu, setActiveMenu] = useState('billing');

  const renderContent = () => {
    switch (activeMenu) {
      case 'billing':
        return (
          <div className="flex-1 p-6">
            <div className="grid grid-cols-1 gap-6">
              <div className="bg-gray-700 rounded-xl shadow-lg border border-gray-800 p-6">
                <h2 className="text-xl font-bold mb-4 text-gray-200 uppercase tracking-wide">Budget</h2>
                <BudgetView />
              </div>
              <div className="bg-gray-700 rounded-xl shadow-lg border border-gray-800 p-6">
                <h2 className="text-xl font-bold mb-4 text-gray-200 uppercase tracking-wide">Repair History</h2>
                <RepairList />
              </div>
            </div>
          </div>
        );
      case 'customers':
        return (
          <div className="flex-1 p-6">
            <div className="bg-gray-700 rounded-xl shadow-lg border border-gray-800 p-6">
              <h2 className="text-xl font-bold mb-4 text-gray-200 uppercase tracking-wide">Customer Cars</h2>
              <CarList />
            </div>
          </div>
        );
      case 'warehouse':
        return (
          <div className="flex-1 p-6">
            <div className="bg-gray-700 rounded-xl shadow-lg border border-gray-800 p-6">
              <h2 className="text-xl font-bold mb-4 text-gray-200 uppercase tracking-wide">Car Parts Inventory</h2>
              <PartList />
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen w-full bg-gray-900 flex">
      <Sidebar activeMenu={activeMenu} onMenuChange={setActiveMenu} />
      {renderContent()}
    </div>
  );
}
