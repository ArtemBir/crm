import React, { useEffect, useState } from "react";
import API from "../api";

export default function BudgetView() {
  const [serviceBudget, setServiceBudget] = useState(0);
  const [customers, setCustomers] = useState([]);
  const [carTypes, setCarTypes] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [budgetResponse, customersResponse, carTypesResponse] = await Promise.all([
        API.get("/accounting/budget/"),
        API.get("/customers/"),
        API.get("/tech/cartypes/")
      ]);
      setServiceBudget(budgetResponse.data[0]?.value ?? 0);
      setCustomers(customersResponse.data);
      setCarTypes(carTypesResponse.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching data:", error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const getCarTypeName = (carTypeId) => {
    const type = carTypes.find(ct => ct.id === carTypeId);
    return type ? `${type.make} ${type.model}` : 'Unknown';
  };

  if (loading) {
    return <div className="p-4 text-gray-200">Loading...</div>;
  }

  return (
    <div className="p-4">
      <div className="border border-gray-800 bg-gray-600 rounded-lg p-4 mb-4 text-gray-200">
        <div className="flex items-center gap-4 text-3xl font-bold">
          <span className="text-gray-200">Service Budget:</span>
          <span className="text-green-400">${serviceBudget}</span>
        </div>
      </div>

      <div className="mt-6">
        <h3 className="text-lg font-semibold mb-4 text-gray-200">Customer Budgets</h3>
        <div className="space-y-4">
          {customers.map(customer => (
            <div key={customer.id} className="border border-gray-800 bg-gray-600 rounded-lg p-4 text-gray-200">
              <div className="flex justify-between items-start gap-4">
                {/* Personal Information */}
                <div className="flex-1">
                  <div className="font-semibold text-lg">{customer.name}</div>
                  <div className="text-sm text-gray-300">Phone: {customer.phone}</div>
                </div>

                {/* Cars List */}
                <div className="flex-1 border-l border-r border-gray-700 px-4">
                  <div className="text-sm font-semibold mb-2">Cars:</div>
                  <ul className="text-sm text-gray-300 space-y-1">
                    {customer.cars.map(car => (
                      <li key={car.id} className="flex items-center gap-2">
                        <span className="w-2 h-2 bg-gray-800 rounded-full"></span>
                        {getCarTypeName(car.car_type)} ({car.year}, {car.color})
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Budget */}
                <div className="flex-1 text-right">
                  <div className="text-sm text-gray-200 font-bold">Budget</div>
                  <div className="text-2xl font-bold text-green-400">${customer.budget || 0}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
