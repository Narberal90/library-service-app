import React from "react";

import "../styles/components/FilterSort.css"

const FilterSortContainer = () => {
    return (
        <div className="filter_sort_container">
            <input className="filter_input" placeholder="filter by"/>
            <select>
                <option disabled>Sort by</option>
                <option>By name</option>
                <option>By date</option>
            </select>
        </div>
    )
}

export default FilterSortContainer
