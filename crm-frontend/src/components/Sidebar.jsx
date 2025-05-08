import React from 'react';

function Sidebar({ activeMenu, onMenuChange }) {
  const menuItems = [
    { id: 'billing', label: 'Billing' },
    { id: 'customers', label: 'Customers' },
    { id: 'warehouse', label: 'Warehouse'}
  ];

  return (
    <div className="w-64 bg-gray-700 min-h-screen p-4">
      <div className="text-xl font-bold text-gray-200 mb-8 text-center">Auto Repair Shop</div>
      <nav>
        <ul className="space-y-2">
          {menuItems.map(item => (
            <li key={item.id}>
              <button
                onClick={() => onMenuChange(item.id)}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors border border-gray-800 ${
                  activeMenu === item.id
                    ? 'bg-gray-600 text-gray-200'
                    : 'bg-gray-800 text-gray-200 hover:bg-gray-700'
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                <span>{item.label}</span>
              </button>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}

export default Sidebar; 