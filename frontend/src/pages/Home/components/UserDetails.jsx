import { Calendar } from "iconsax-react";
import React from "react";

function UserDetails() {
  return (
    <div>
      <div className="flex gap-4 mb-8">
        <div className="h-16 w-16 bg-gray-200 rounded-full"></div>
        <div className="flex gap-10 items-end">
          <div>
            <h3 className="font-black text-4xl">Hi, John</h3>
            <span className="flex text-gray-700 gap-2">
              <Calendar /> You're doing great! 2 hours driven
            </span>
          </div>
          <button className="bg-gray-900 hover:bg-black transition-all rounded-md text-lg font-bold text-white py-1.5 px-10 h-fit">Start Trip</button>
        </div>
      </div>
    </div>
  );
}

export default UserDetails;
