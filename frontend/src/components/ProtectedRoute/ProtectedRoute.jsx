import React from "react";
import { EuiLoadingSpinner } from "@elastic/eui";
import { LoginPage } from "components";
import { useProtectedRoute } from "hooks/auth/useProtectedRoute";

const ProtectedRoute = ({ component: Component, ...props }) => {
  const { isAuthenticated, userLoaded } = useProtectedRoute();

  if (!userLoaded) return <EuiLoadingSpinner size="xl" />;

  if (!isAuthenticated) return <LoginPage />;

  return <Component {...props} />;
};

export default ProtectedRoute;
