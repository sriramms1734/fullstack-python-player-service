import React, { useEffect } from "react";
import usePagination from "../utils/usePagination";

const Pagination = (props) => {
  const { pageNumber, changePage, pageData, nextPage, previousPage } =
    usePagination(props.items, props.pageLimit);

  useEffect(() => {
    props.setPageItems(pageData);
  }, [pageNumber]);

  return (
    <div>
      <b onClick={previousPage}>Prev</b>
      <input
        value={pageNumber}
        onChange={(e) => {
          changePage(e.target.valueAsNumber);
        }}
        type="number"
      />
      <b onClick={nextPage}>Next</b>
    </div>
  );
};

export default Pagination;