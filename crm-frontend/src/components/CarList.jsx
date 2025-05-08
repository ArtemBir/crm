import React, { useEffect, useState } from "react";
import API from "../api";

function CarList() {
  const [cars, setCars] = useState([]);
  const [carTypes, setCarTypes] = useState([]);
  const [parts, setParts] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [selectedParts, setSelectedParts] = useState({});

  const fetchCars = async () => {
    const response = await API.get("/tech/");
    setCars(response.data);
  };

  const fetchCarTypes = async () => {
    const response = await API.get("/tech/cartypes/");
    setCarTypes(response.data);
  };

  const fetchParts = async () => {
    const response = await API.get("/tech/carparts/");
    setParts(response.data);
  };

  const fetchCustomers = async () => {
    const response = await API.get("/customers/");
    setCustomers(response.data);
  };

  const startRepair = async (carId, partId) => {
    try {
      if (!carId || !partId) {
        alert("Please select both a car and a part");
        return;
      }

      const car = cars.find(c => c.id === carId);
      if (car && ([car.state, car.state_display].some(s => String(s).toLowerCase().replace(/\s/g, '') === 'inservice'))) {
        alert("This car is already in service");
        return;
      }

      const part = parts.find(p => p.id === partId);
      if (part && !part.in_stock) {
        alert("This part is not in stock");
        return;
      }

      if (part && part.car_type && part.car_type !== car.car_type) {
        alert("This part is not compatible with this car type");
        return;
      }

      // Find customer who owns this car
      const customer = customers.find(c => c.cars.some(car => car.id === carId));
      if (!customer) {
        alert("Could not find the car's owner");
        return;
      }

      // Check if customer has enough budget
      if (customer.budget < part.price) {
        alert("Customer does not have enough budget for this repair");
        return;
      }

      await API.post("/tech/repair/start/", {
        car_id: carId,
        car_part_id: partId
      });
      await Promise.all([
        fetchCars(),
        fetchParts(),
        fetchCustomers()
      ]);
      alert("Repair started successfully!");
    } catch (error) {
      console.error("Repair start error:", error);
      let errorMessage = "Failed to start repair. ";
      
      if (error.response?.data) {
        if (typeof error.response.data === 'string' && error.response.data.includes("Exception Value:")) {
          const match = error.response.data.match(/Exception Value:\s*<pre>(.*?)<\/pre>/);
          errorMessage += match ? match[1].trim() : "Unknown error";
        } else if (typeof error.response.data === 'object' && error.response.data.detail) {
          errorMessage += error.response.data.detail;
        } else {
          errorMessage += "Please try again.";
        }
      }
      
      alert(errorMessage);
    }
  };

  const finishRepair = async (carId) => {
    try {
      await API.post("/tech/repair/finish/", {
        car_id: carId,
        car_part_id: partId
      });
      alert("Repair finished!");
      await Promise.all([
        fetchCars(),
        fetchCustomers()
      ]);
    } catch (error) {
      console.error("Repair finish error:", error, error.response?.data);
      let errorMessage = "Failed to finish repair. ";
      
      if (error.response?.data) {
        if (typeof error.response.data === 'string' && error.response.data.includes("Exception Value:")) {
          const match = error.response.data.match(/Exception Value:\s*<pre>(.*?)<\/pre>/);
          errorMessage += match ? match[1].trim() : "Unknown error";
        } else if (typeof error.response.data === 'object' && error.response.data.detail) {
          errorMessage += error.response.data.detail;
        } else {
          errorMessage += "Please try again.";
        }
      }
      
      alert(errorMessage);
    }
  };

  useEffect(() => {
    fetchCars();
    fetchCarTypes();
    fetchParts();
    fetchCustomers();
    const interval = setInterval(() => {
      fetchCars();
      fetchCarTypes();
      fetchParts();
      fetchCustomers();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const getCarType = (carTypeId) => carTypes.find(ct => ct.id === carTypeId);
  const getCustomerName = (carId) => {
    const customer = customers.find(c => c.cars.some(car => car.id === carId));
    return customer ? customer.name : "Unknown";
  };

  return (
    <div className="p-4">
      <ul className="space-y-4">
        {cars
          .sort((a, b) => a.id - b.id)
          .map(car => {
          const carType = getCarType(car.car_type);
          const selectedPartId = selectedParts[car.id] || "";
          const isInService = [car.state, car.state_display].some(s => String(s).toLowerCase().replace(/\s/g, '') === 'inservice');
          
          return (
            <li key={car.id} className="border border-gray-800 bg-gray-600 rounded-lg p-4 mb-4">
              <div className="flex gap-4">
                <div className="flex-1 text-gray-200">
                  <div><b>ID:</b> {car.id}</div>
                  <div><b>Owner:</b> {getCustomerName(car.id)}</div>
                  <div><b>Type:</b> {carType ? `${carType.make} ${carType.model}` : "—"}</div>
                  <div><b>Year:</b> {car.year}</div>
                  <div><b>Color:</b> {car.color}</div>
                  <div>
                    <b>State:</b>{' '}
                    <span className={
                      isInService
                        ? 'text-red-500'
                        : ([car.state, car.state_display].some(s => String(s).toLowerCase().replace(/\s/g, '') === 'noservice'))
                        ? 'text-green-500'
                        : ''
                    }>
                      {car.state_display || car.state}
                    </span>
                  </div>
                  <div className="mt-2">
                    <select
                      className="bg-gray-700 border border-gray-500 text-gray-200 rounded px-2 py-1 w-full"
                      value={selectedParts[car.id] || ""}
                      onChange={e => setSelectedParts({ ...selectedParts, [car.id]: Number(e.target.value) })}
                    >
                      <option value="">Select part</option>
                      {parts
                        .filter(part => !part.car_type || part.car_type === car.car_type)
                        .map(part => (
                          <option key={part.id} value={part.id}>
                            {part.name} (id: {part.id}) - ${part.price}
                          </option>
                        ))}
                    </select>
                  </div>
                </div>
                <div className="flex flex-col gap-2 justify-center">
                  <button
                    onClick={() => startRepair(car.id, selectedParts[car.id])}
                    className="h-[calc(50%-4px)] px-4 bg-green-700 text-gray-200 rounded hover:bg-green-600 transition-colors"
                    disabled={!selectedParts[car.id]}
                  >
                    Start Repair
                  </button>
                  <button
                    onClick={() => finishRepair(car.id)}
                    className="h-[calc(50%-4px)] px-4 bg-red-800 text-gray-200 rounded hover:bg-red-700 transition-colors"
                    disabled={!isInService}
                  >
                    Finish Repair
                  </button>
                </div>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default CarList;
