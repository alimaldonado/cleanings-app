import React from "react";
import {
  EuiIcon,
  EuiHeader,
  EuiHeaderSection,
  EuiHeaderSectionItem,
  EuiHeaderLink,
} from "@elastic/eui";
import styled from "styled-components";

const LogoSection = styled(EuiHeaderLink)`
  padding: 0 2rem;
`;

const Navbar = ({ ...props }) => {
  return (
    <EuiHeader style={props.style || {}}>
      <EuiHeaderSection>
        <LogoSection href="">
          <EuiIcon type="cloudDrizzle" color="#1E90FF" size="1" />
          Phresh
        </LogoSection>
      </EuiHeaderSection>
    </EuiHeader>
  );
};

export default Navbar;
