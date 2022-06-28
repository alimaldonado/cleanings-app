import React, { useState } from "react";
import {
  EuiAvatar,
  EuiIcon,
  EuiHeader,
  EuiHeaderSection,
  EuiHeaderSectionItem,
  EuiHeaderSectionItemButton,
  EuiHeaderLinks,
  EuiHeaderLink,
  EuiPopover,
  EuiFlexGroup,
  EuiFlexItem,
  EuiLink,
} from "@elastic/eui";
import { Link, useNavigate } from "react-router-dom";
import styled from "styled-components";

import loginIcon from "../../assets/img/loginIcon.svg";
import { useAuthenticatedUser } from "hooks/auth/useAuthenticatedUser";
import { UseAvatar } from "components";

const LogoSection = styled(EuiHeaderLink)`
  padding: 0 2rem;
`;

const AvatarMenu = styled.div`
  display: flex;
  justify-content: space-between;
  min-width: 300px;

  & .avatar-actions {
    margin-left: 2rem;
  }
`;

const Navbar = ({ ...props }) => {
  const [avatarMenuOpen, setAvatarMenuOpen] = useState(false);
  const { user, logUserOut } = useAuthenticatedUser();
  const navigate = useNavigate();

  const toggleAvatarMenu = () => setAvatarMenuOpen(!avatarMenuOpen);
  const closeAvatarMenu = () => setAvatarMenuOpen(false);

  const handleLogout = () => {
    closeAvatarMenu();
    logUserOut();
    navigate("/");
  };

  const avatarButton = (
    <EuiHeaderSectionItemButton
      aria-label="User avatar"
      onClick={() => user?.profile && toggleAvatarMenu()}
    >
      {user?.profile ? (
        <UseAvatar size="l" user={user} initialsLength={2} />
      ) : (
        <Link to="/login">
          <EuiAvatar size="l" name="user" imageUrl={loginIcon} />
        </Link>
      )}
    </EuiHeaderSectionItemButton>
  );

  const renderAvatarMenu = () => {
    if (!user?.profile) return null;

    return (
      <AvatarMenu>
        <UseAvatar size="xl" user={user} initialsLength="2" />
        <EuiFlexGroup direction="column" className="avatar-actions">
          <EuiFlexItem grow={1}>
            <p>
              {user.email} - {user.username}{" "}
            </p>
          </EuiFlexItem>
          <EuiFlexItem grow={1}>
            <EuiFlexGroup justifyContent="spaceBetween">
              <EuiFlexItem grow={1}>
                <Link to="/profile">Profile</Link>
              </EuiFlexItem>
              <EuiFlexItem grow={1}>
                <EuiLink onClick={() => handleLogout()}>Log Out</EuiLink>
              </EuiFlexItem>
            </EuiFlexGroup>
          </EuiFlexItem>
        </EuiFlexGroup>
      </AvatarMenu>
    );
  };
  return (
    <EuiHeader style={props.style || {}}>
      <EuiHeaderSection>
        <EuiHeaderSectionItem border="right">
          <LogoSection href="/">
            <EuiIcon type="cloudDrizzle" color="#1E90FF" size="l" /> Phresh
          </LogoSection>
        </EuiHeaderSectionItem>
        <EuiHeaderSectionItem border="right">
          <EuiHeaderLinks aria-label="app navigation links">
            <EuiHeaderLink iconType="tear" href="#">
              Find Cleaners
            </EuiHeaderLink>
            <EuiHeaderLink iconType="tag">
              <Link to={"/cleaning-jobs"}>Find Jobs</Link>
            </EuiHeaderLink>
            <EuiHeaderLink iconType="help" href="#">
              Help
            </EuiHeaderLink>
          </EuiHeaderLinks>
        </EuiHeaderSectionItem>
      </EuiHeaderSection>
      <EuiHeaderSection>
        <EuiPopover
          id="avatar-menu"
          isOpen={avatarMenuOpen}
          closePopover={closeAvatarMenu}
          anchorPosition="downRight"
          button={avatarButton}
          panelPaddingSize="l"
        >
          {renderAvatarMenu()}
        </EuiPopover>
      </EuiHeaderSection>
    </EuiHeader>
  );
};

export default Navbar;
