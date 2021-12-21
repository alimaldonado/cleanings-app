import { EuiEmptyPrompt } from "@elastic/eui";
import React from "react";

const PermissionsNeeded = ({ element, isAllowed = false }) => {
  if (!isAllowed) {
    return (
      <EuiEmptyPrompt
        iconType={"securityApp"}
        iconColor={null}
        title={<h2>Access Denied</h2>}
        body={<p>You are not allowed to access this content.</p>}
      />
    );
  }
  return element;
};

export default PermissionsNeeded;
