import React from "react";
import {
  CleaningJobsHome,
  NotFoundPage,
  CleaningJobView,
} from "../../components";
import { Routes, Route } from "react-router-dom";

const CleaningJobsPage = () => {
  return (
    <>
      <Routes>
        <Route path="/" element={<CleaningJobsHome />} />
        <Route path=":cleaning_id" element={<CleaningJobView />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </>
  );
};

export default CleaningJobsPage;
