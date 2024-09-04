/*

****** Using this file for code review only. This is not a part of the project. ******


import React, { useState, useEffect } from "react";
import { FilterBoxProps, Filter } from "../../types/interface";

export default function FilterBox({
  columns,
  onRemoveFilter,
  index,
  updateFilter,
}: FilterBoxProps) {
  const [selectedColumn, setSelectedColumn] = useState<string>("");
  const [condition, setCondition] = useState<string>("");
  const [value, setValue] = useState<string>("");

  useEffect(() => {
    const newFilter: Filter = { column: selectedColumn, condition, value };
    updateFilter(index, newFilter);
  }, [selectedColumn, condition, value]);

  return (
    <div className="p-4 bg-white rounded-lg shadow-md">
      <div className="flex flex-row items-center">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">
          Filter {index + 1}
        </h2>
        <button
          className="text-black ml-auto mb-auto text-2xl"
          onClick={onRemoveFilter}
        >
          &times;
        </button>
      </div>

      <div className="flex flex-col gap-4 text-gray-700">
        <select
          className="p-2 border border-gray-300 rounded"
          value={selectedColumn}
          onChange={(e) => setSelectedColumn(e.target.value)}
        >
          <option value="" disabled>
            Select column
          </option>
          {columns.map((column) => (
            <option key={column} value={column}>
              {column}
            </option>
          ))}
        </select>

        <select
          className="p-2 border border-gray-300 rounded"
          value={condition}
          onChange={(e) => setCondition(e.target.value)}
        >
          <option value="" disabled>
            Select condition
          </option>
          <option value="equals">Equals</option>
          <option value="not equals">Not Equals</option>
          <option value="contains">Contains</option>
          <option value="does not contain">Does Not Contain</option>
          <option value="greater than">Greater Than</option>
          <option value="less than">Less Than</option>
        </select>

        <input
          type="text"
          className="p-2 border border-gray-300 rounded"
          placeholder="Enter value"
          value={value}
          onChange={(e) => setValue(e.target.value)}
        />
      </div>
    </div>
  );
}

*/

