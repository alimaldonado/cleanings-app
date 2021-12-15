import React from "react";
import { CleaningJobsHome, NotFoundPage } from "../../components";
import { Routes, Route } from "react-router-dom";

const CleaningJobsPage = () => {
  return (
    <>
      <Routes>
        <Route path="/" element={<CleaningJobsHome />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </>
  );
};

export default CleaningJobsPage;
