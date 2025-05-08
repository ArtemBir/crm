import React, { useEffect, useState } from "react";
import API from "../api";

export default function PartList() {
  const [parts, setParts] = useState([]);
  const [carTypes, setCarTypes] = useState([]);
  const [purchaseQuantities, setPurchaseQuantities] = useState({}); // partId -> quantity

  useEffect(() => {
    API.get("/tech/carparts/").then((response) => {
      const sortedParts = [...response.data].sort((a, b) => {
        if (a.in_stock === 0 && b.in_stock > 0) return 1;
        if (a.in_stock > 0 && b.in_stock === 0) return -1;
        return 0;
      });
      setParts(sortedParts);
    });
    API.get("/tech/cartypes/").then((response) => {
      setCarTypes(response.data);
    });
    const interval = setInterval(() => {
      API.get("/tech/carparts/").then((response) => {
        const sortedParts = [...response.data].sort((a, b) => {
          if (a.in_stock === 0 && b.in_stock > 0) return 1;
          if (a.in_stock > 0 && b.in_stock === 0) return -1;
          return 0;
        });
        setParts(sortedParts);
      });
      API.get("/tech/cartypes/").then((response) => {
        setCarTypes(response.data);
      });
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleQuantityChange = (partId, value) => {
    const quantity = parseInt(value) || 0;
    setPurchaseQuantities(prev => ({
      ...prev,
      [partId]: quantity
    }));
  };

  const purchaseParts = async (partId) => {
    const quantity = purchaseQuantities[partId] || 0;
    if (quantity <= 0) {
      alert("Please enter a valid quantity");
      return;
    }

    try {
      await API.post(`/tech/carparts/${partId}/purchase/`, {
        quantity: quantity
      });
      
      const response = await API.get("/tech/carparts/");
      const sortedParts = [...response.data].sort((a, b) => {
        if (a.in_stock === 0 && b.in_stock > 0) return 1;
        if (a.in_stock > 0 && b.in_stock === 0) return -1;
        return 0;
      });
      setParts(sortedParts);
      
      setPurchaseQuantities(prev => ({
        ...prev,
        [partId]: 0
      }));
      
      alert("Parts purchased successfully!");
    } catch (error) {
      console.error("Error purchasing parts:", error);
      if (error.response?.data?.detail) {
        alert(`Failed to purchase parts: ${error.response.data.detail}`);
      } else {
        alert("Failed to purchase parts. Please try again.");
      }
    }
  };

  const getCarTypeName = (id) => {
    const type = carTypes.find(ct => ct.id === id);
    return type ? `${type.make} ${type.model}` : id;
  };

  return (
    <div className="p-4">
      <ul className="space-y-4">
        {parts
          .sort((a, b) => {
            // First sort by stock status
            if (a.in_stock === 0 && b.in_stock > 0) return 1;
            if (a.in_stock > 0 && b.in_stock === 0) return -1;
            // Then sort by ID
            return a.id - b.id;
          })
          .map(part => (
          <li key={part.id} className="border border-gray-800 bg-gray-600 rounded-lg p-4 mb-4 text-gray-200">
            <div className="flex gap-4">
              <div className="flex-1 text-gray-200">
                <div><b>ID:</b> {part.id}</div>
                <div>Part: {part.name}</div>
                <div>
                  In stock:{' '}
                  <span className={`${part.in_stock > 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {part.in_stock} {part.in_stock === 1 ? 'piece' : 'pieces'}
                  </span>
                </div>
                <div>Price: ${part.price}</div>
                {part.car_type && (
                  <div>Fits car type: {getCarTypeName(part.car_type)}</div>
                )}
              </div>
              <div className="flex flex-col w-32">
                <input
                  type="number"
                  min="0"
                  value={purchaseQuantities[part.id] || ''}
                  onChange={(e) => handleQuantityChange(part.id, e.target.value)}
                  className="w-full bg-gray-700 border border-gray-500 text-gray-200 rounded px-2 py-1"
                  placeholder="Quantity"
                />
                <button
                  onClick={() => purchaseParts(part.id)}
                  className="w-full px-4 py-1 bg-blue-500 text-gray-200 rounded hover:bg-blue-600 transition-colors mt-2 flex-1"
                  disabled={!purchaseQuantities[part.id] || purchaseQuantities[part.id] <= 0}
                >
                  Purchase
                </button>
                {purchaseQuantities[part.id] > 0 && (
                  <div className="text-sm text-gray-300 mt-2">
                    Total: ${(part.price * purchaseQuantities[part.id]).toFixed(2)}
                  </div>
                )}
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
