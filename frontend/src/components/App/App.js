import React from "react";
import { LandingPage, Layout } from "../../components";

import { EuiText } from "@elastic/eui";

export default function App() {
  return (
    <Layout>
      <EuiText>
        <LandingPage />
      </EuiText>
    </Layout>
  );
}
