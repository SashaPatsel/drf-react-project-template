import React from "react";

const Pagination = ({ postsPerPage, totalPosts, paginate, activeNumber }) => {
  const pageNumbers = []

  const totalPages = Math.ceil(totalPosts / postsPerPage)
  // Gets the number of pages
  for (let i = 1; i <= totalPages; i++) {
    let wasPushed = false
    // only push five pages, make sure the active page is in the middle (if possible)
    if (i > activeNumber - 3 && i < activeNumber + 3 && pageNumbers.length < 5) {
      pageNumbers.push(i)
      wasPushed = true
    }

    // Make sure there's still five options at the beginning of the number list
    if (activeNumber < 3 && !wasPushed && pageNumbers.length < 5) {
      pageNumbers.push(i)
      wasPushed = true
    }

    // Make sure there's still five options at the end of the number list
    if (i > totalPages - 5 && !wasPushed && pageNumbers.length < 5) {
      pageNumbers.push(i)
    }
    
  }
  return (
    <nav>
      <ul className="pagination">
        <li  onClick={activeNumber > 1 ? () => paginate(1) : null} className={`pagination__item ${activeNumber > 1 ? "" : "pagination__item--inactive"}`}>
          <div className="pagination__link">
          <i className="fas fa-angle-double-left"></i>
          </div>
        </li>
        <li onClick={activeNumber > 1 ? () => paginate(activeNumber - 1) : null} className={`pagination__item ${activeNumber > 1 ? "" : "pagination__item--inactive"}`}>
          <div className="pagination__link">
            <i className="fas fa-chevron-left"></i>
          </div>
        </li>

        {pageNumbers.map(number => (
          <li onClick={() => paginate(number)} key={number} className={`pagination__item ${number === activeNumber ? "pagination__item--active" : ""}`}>
            <div className="pagination__link">
              {number}
            </div>
          </li>
        ))}

        <li onClick={activeNumber < totalPages ? () => paginate(activeNumber + 1) : null} className={`pagination__item ${activeNumber < totalPages ? "" : "pagination__item--inactive"}`}>
          <div className="pagination__link">
            <i className="fas fa-chevron-right"></i>
          </div>
        </li>
        <li onClick={activeNumber < totalPages ? () => paginate(totalPages) : null}  className={`pagination__item ${activeNumber < totalPages ? "" : "pagination__item--inactive"}`}>
          <div className="pagination__link">
          <i className="fas fa-angle-double-right"></i>
          </div>
        </li>
      </ul>
    </nav>
  )

}
export default Pagination
