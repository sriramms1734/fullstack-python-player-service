import React, { useState } from "react";

const PaginatedPlayers = ({ players, itemsPerPage }) => {
  // State to track the current page
  const [currentPage, setCurrentPage] = useState(1);

  // Calculate total pages
  const totalPages = Math.ceil(players.length / itemsPerPage);

  // Get the players for the current page
  const currentPlayers = players.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  // Handlers for pagination controls
  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  return (
    <div className="players-results-section">
      {/* Results section */}
      {currentPlayers.map((player) => (
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
          disabled={currentPage === 1}
        >
          Previous
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button
          onClick={handleNextPage}
          disabled={currentPage === totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default PaginatedPlayers;
