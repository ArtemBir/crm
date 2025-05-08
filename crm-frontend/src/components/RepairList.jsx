import React, { useEffect, useState } from "react";
import API from "../api";

export default function RepairList() {
  const [repairs, setRepairs] = useState([]);
  const [parts, setParts] = useState([]);
  const [customers, setCustomers] = useState([]);

  useEffect(() => {
    API.get("/tech/repair/").then((response) => {
      setRepairs(response.data);
    });
    API.get("/tech/carparts/").then((response) => {
      setParts(response.data);
    });
    API.get("/customers/").then((response) => {
      setCustomers(response.data);
    });
    const interval = setInterval(() => {
      API.get("/tech/repair/").then((response) => {
        setRepairs(response.data);
      });
      API.get("/tech/carparts/").then((response) => {
        setParts(response.data);
      });
      API.get("/customers/").then((response) => {
        setCustomers(response.data);
      });
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const deleteRepair = async (repairId) => {
    try {
      await API.delete(`/tech/repair/delete/${repairId}/`);
      const response = await API.get("/tech/repair/");
      setRepairs(response.data);
    } catch (error) {
      console.error("Error deleting repair:", error);
      alert("Failed to delete repair");
    }
  };

  const getPartName = (id) => {
    const part = parts.find(p => p.id === id);
    return part ? part.name : id;
  };

  const getCustomerName = (customerId) => {
    const customer = customers.find(c => c.id === customerId);
    return customer ? `${customer.name} (${customer.phone})` : 'Unknown';
  };

  return (
    <div className="p-4">
      <ul className="space-y-4">
        {repairs
          .sort((a, b) => a.id - b.id)
          .map(repair => (
          <li key={repair.id} className="border border-gray-800 bg-gray-600 rounded-lg p-4 mb-4 text-gray-200 flex items-center justify-between gap-4">
            <div>
              <div>Car ID: {repair.car}</div>
              <div>Customer: {getCustomerName(repair.customer)}</div>
              <div>Parts used: {repair.car_parts.map(id => {
                const part = parts.find(p => p.id === id);
                return part ? `${part.name} (id: ${part.id})` : `id: ${id}`;
              }).join(", ")}</div>
              <div>Price: ${repair.expense}</div>
            </div>
            <button
              onClick={() => {
                if (window.confirm('Are you sure you want to delete this repair?')) {
                  deleteRepair(repair.id);
                }
              }}
              className="bg-red-800 text-gray-200 rounded px-4 py-2 hover:bg-red-700 transition-colors"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
