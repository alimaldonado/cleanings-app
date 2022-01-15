import React from "react";
import styled from "styled-components";
import {
  EuiAvatar,
  EuiBasicTable,
  EuiButton,
  EuiEmptyPrompt,
  EuiFlexGroup,
  EuiFlexItem,
  EuiHealth,
  EuiPanel,
} from "@elastic/eui";
import moment from "moment";

const Wrapper = styled(EuiPanel)`
  max-width: 800px;
  margin: 1rem auto;
  padding: 2rem;
`;

const UserAvatar = styled.div`
  display: flex;
  align-items: center;

  & > strong {
    margin-left: 0.6rem;
  }
`;

const StyledH3 = styled.h3`
  margin-bottom: 1.5rem;
  font-weight: bold;
`;

const renderStatus = (status) => {
  const color = {
    accepted: "success",
    pending: "primary",
    rejected: "danger",
  }[status || "pending"];
  return <EuiHealth color={color}>{status}</EuiHealth>;
};

const emptyOffersMessage = (
  <EuiEmptyPrompt
    title={<h3>No Offers</h3>}
    titleSize="xs"
    body={`Looks like you don't have any offers yet`}
  />
);

const capitalize = (str) => (str ? str[0].toUpperCase() + str.slice(1) : str);

const Table = ({
  offers,
  offersIsUpdating,
  offersIsLoading,
  handleAcceptOffer,
}) => {
  const columns = [
    {
      field: `user`,
      name: `User`,
      sortable: true,
      truncateText: true,
      mobileOptions: {
        render: (item) => <strong>{capitalize(item.user?.username)}</strong>,
      },
      render: (user) => (
        <UserAvatar>
          <EuiAvatar
            size="m"
            name={
              user?.profile?.full_name ||
              user?.username?.toUpperCase() ||
              "Anonymous"
            }
            initialsLength={1}
            imageUrl={user?.profile?.image}
          />
          <strong>{capitalize(user?.username)}</strong>
        </UserAvatar>
      ),
    },
    {
      field: "created_at",
      name: "Sent At",
      truncateText: false,
      mobileOptions: {
        // Custom renderer for mobile view only
        render: (item) => (
          <>{moment(new Date(item.created_at)).format("MM-DD-YYYY")}</>
        ),
      },
      render: (created_at) => (
        <>{moment(new Date(created_at)).format("MMMM do, YYYY")}</>
      ),
    },
    {
      field: "status",
      name: "Status",
      truncateText: false,
      render: (status) => <>{renderStatus(status)}</>,
    },
    {
      name: "Actions",
      actions: [
        {
          available: ({ status }) => status === "pending",
          width: "100%",
          render: ({ user, cleaning_id }) => (
            <EuiButton
              isLoading={offersIsUpdating || offersIsLoading}
              onClick={() =>
                handleAcceptOffer({ username: user.username, cleaning_id })
              }
              color="secondary"
              fill
            >
              Accept Offer
            </EuiButton>
          ),
        },
      ],
    },
  ];

  offers.forEach((offer) => {
    console.log(offer);
  });

  return (
    <Wrapper>
      <EuiFlexGroup>
        <EuiFlexItem>
          <StyledH3>Offers</StyledH3>
        </EuiFlexItem>
      </EuiFlexGroup>
      <EuiBasicTable
        items={offers}
        itemId="user_id"
        columns={columns}
        hasActions={false}
        message={offers?.length ? null : emptyOffersMessage}
        rowHeader="user"
      />
    </Wrapper>
  );
};

export default Table;
