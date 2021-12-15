import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import {
  LandingPage,
  CleaningJobsPage,
  Layout,
  LoginPage,
  NotFoundPage,
  ProfilePage,
  RegistrationPage,
  ProtectedRoute,
} from "../../components";

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route
            path="/cleaning-jobs"
            element={<ProtectedRoute component={CleaningJobsPage} />}
          />
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/profile"
            element={<ProtectedRoute component={ProfilePage} />}
          />
          <Route path="/registration" element={<RegistrationPage />} />
          <Route path="/*" element={<NotFoundPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
