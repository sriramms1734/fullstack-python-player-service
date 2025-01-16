import React, { useContext, useState } from "react";
import { MyContext } from "../Provider";

function usePagination(items, pageLimit) {
  const [pageNumber, setPageNumber] = useState(0);
  const pageCount = Math.ceil(items.length / pageLimit);
  const {fullStore, setFullStore} = useContext(MyContext)

  const changePage = (pN) => {
    if(!isNaN(pN)){
        setFullStore({
            ...fullStore, 
            offset: (pN*10)
        })
    }
        setPageNumber(pN);

  };

  const pageData = () => {
    const s = pageNumber * pageLimit;
    const e = s + pageLimit;
    return items.slice(s, e);
  };

  const nextPage = () => {
    setPageNumber(Math.min(pageNumber + 1, pageCount - 1));
setFullStore({
    ...fullStore, 
    offset: fullStore.offset+10
})
  };

  const previousPage = () => {
    setPageNumber(Math.max(pageNumber - 1, 0));
    setFullStore({
        ...fullStore, 
        offset: fullStore.offset-10
    })
  };

  return {
    pageNumber,
    pageCount,
    changePage,
    pageData,
    nextPage,
    previousPage,
  };
}

export default usePagination;
