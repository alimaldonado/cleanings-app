import React from "react";
import {
  EuiBadge,
  EuiButton,
  EuiCard,
  EuiFlexGroup,
  EuiFlexItem,
  EuiText,
  EuiSpacer,
  EuiLoadingChart,
} from "@elastic/eui";
import styled from "styled-components";
import { shallowEqual, useSelector } from "react-redux";

const ImageHolder = styled.div`
  min-width: 400px;
  min-height: 200px;

  & > img {
    position: relative;
    z-index: 2;
  }
`;

const cleaningTypeToDisplayNameMapping = {
  dust_up: "Dust Up",
  spot_clean: "Spot Clean",
  full_clean: "Full Clean",
};

const CleaningJobCard = ({
  cleaningJob,
  user,
  isOwner,
  offersError,
  offersIsLoading,
  createOfferForCleaning,
}) => {
  const userOfferForCleaningJob = useSelector(
    (state) =>
    state.offers.data?.[cleaningJob?.id]?.[user?.id],
    shallowEqual
  );

  const image = (
    <ImageHolder>
      <EuiLoadingChart size="xl" style={{ position: "absolute", zIndex: 1 }} />
      <img
        src="https://source.unsplash.com/400x200/?Soap"
        alt="Cleaning Job Cover"
      />
    </ImageHolder>
  );

  const title = (
    <EuiFlexGroup justifyContent="spaceBetween" alignItems="center">
      <EuiFlexItem grow={false}> {cleaningJob.name} </EuiFlexItem>
      <EuiFlexItem grow={false}>
        <EuiBadge color="secondary">
          {cleaningTypeToDisplayNameMapping[cleaningJob.cleaning_type]}
        </EuiBadge>
      </EuiFlexItem>
    </EuiFlexGroup>
  );

  const footer = (
    <>
      <EuiSpacer />
      <EuiFlexGroup justifyContent="spaceBetween" alignItems="flexEnd">
        <EuiFlexItem grow={false}>
          <EuiText>{`Hourly Rate: ${cleaningJob.price}`}</EuiText>
        </EuiFlexItem>

        <EuiFlexItem grow={false}>
          {isOwner || userOfferForCleaningJob ? null : (
            <EuiButton
              onClick={() => {
                createOfferForCleaning({ cleaning_id: cleaningJob.id });
              }}
              isLoading={offersIsLoading}
            >
              Offer Services
            </EuiButton>
          )}
        </EuiFlexItem>
      </EuiFlexGroup>
    </>
  );

  const betaBadgeLabel = userOfferForCleaningJob
    ? `Offer ${userOfferForCleaningJob.status}`.toUpperCase()
    : null;

  const betaBadgeTooltipContent = userOfferForCleaningJob
    ? `Offer sent on ${new Date(
        userOfferForCleaningJob.created_at
      ).toLocaleDateString("en-us", {
        year: "numeric",
        month: "long",
        day: "numeric",
      })}`
    : null;

  return (
    <EuiCard
      display="plain"
      textAlign="left"
      image={image}
      title={title}
      description={cleaningJob.description}
      footer={footer}
      betaBadgeProps={{
        label: betaBadgeLabel,
        tooltipContent: betaBadgeTooltipContent,
      }}
    />
  );
};

export default CleaningJobCard;
