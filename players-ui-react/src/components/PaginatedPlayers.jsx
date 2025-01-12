import React, { useState } from "react";

const PaginatedPlayers = ({ moveToNextpage, moveToPrevpage,  players, itemsPerPage }) => {
  // State to track the current page
  const [currentPage, setCurrentPage] = useState(1);

  // Calculate total pages

  // Handlers for pagination controls
  const handleNextPage = () => {
      moveToNextpage();
      setCurrentPage(currentPage + 1);
  };

  const handlePreviousPage = () => {
      moveToPrevpage();
      setCurrentPage(currentPage - 1);
  };

  return (
    <div className="players-results-section">
      {/* Results section */}
      {players.map((player) => (
        <div
          key={player.playerId}
          style={{ display: "flex", gap: "1vh" }}
        >
          <div>{player.playerId}</div>
          <div>{player.birthCountry}</div>
        </div>
      ))}

      {/* Pagination controls */}
      <div style={{ marginTop: "2vh", display: "flex", gap: "1vh" }}>
        <button
          onClick={handlePreviousPage}
          disabled={currentPage<=0}
        >
          Previous
        </button>
        <span>
          Page {currentPage}
        </span>
        <button
          onClick={handleNextPage}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default PaginatedPlayers;
