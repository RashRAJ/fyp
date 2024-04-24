import React from "react";

function Card({ children }) {
  return <div className="bg-transparen w-full rounded-xl opacity-1 border border-gray-200 px-8 flex justify-between flex-col z-20 my-2">{children}</div>;
}

export default Card;
