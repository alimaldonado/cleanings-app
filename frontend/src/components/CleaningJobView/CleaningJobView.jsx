import React, { useEffect } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import { connect, useSelector, shallowEqual } from "react-redux";
import {
  EuiPage,
  EuiPageBody,
  EuiPageContent,
  EuiPageContentBody,
  EuiLoadingSpinner,
  EuiFlexGroup,
  EuiFlexItem,
  EuiAvatar,
  EuiTitle,
  EuiButtonIcon,
  EuiButtonEmpty,
} from "@elastic/eui";
import { useParams } from "react-router-dom";
import styled from "styled-components";
import { Actions as cleaningActions } from "../../redux/cleanings";
import { Actions as offersActions } from "../../redux/offers";
import {
  CleaningJobCard,
  CleaningJobEditForm,
  NotFoundPage,
  PermissionsNeeded,
  CleaningJobOffersTable,
} from "../../components";

const StyledEuiPage = styled(EuiPage)`
  flex: 1;
`;

const StyledFlexGroup = styled(EuiFlexGroup)`
  padding: 1rem;
`;

const CleaningJobView = ({
  user,
  isLoading,
  cleaningError,
  currentCleaningJob,
  fetchCleaningJobById,
  clearCurrentCleaningJob,

  offersError,
  offersIsLoading,
  offersIsUpdating,
  createOfferForCleaning,
  fetchUserOfferForCleaningJob,
  fetchAllOffersForCleaningJob,
  acceptUsersOfferForCleaningJob,
}) => {
  const { cleaning_id } = useParams();

  const navigate = useNavigate();

  const userOwnsCleaningResource = useSelector(
    (state) => state.cleanings.data?.[cleaning_id]?.owner === user?.id,
    shallowEqual
  );

  const allOffersForCleaningJob = useSelector(
    (state) => state.offers.data?.[cleaning_id],
    shallowEqual
  );

  useEffect(() => {
    if (cleaning_id && user?.username) {
      fetchCleaningJobById({ cleaning_id });

      if (userOwnsCleaningResource) {
        fetchAllOffersForCleaningJob({ cleaning_id });
      } else {
        fetchUserOfferForCleaningJob({ cleaning_id, username: user.username });
      }
    }
    console.log(userOwnsCleaningResource);
    return () => clearCurrentCleaningJob();
    // eslint-disable-next-line
  }, [
    cleaning_id,
    fetchCleaningJobById,
    clearCurrentCleaningJob,
    userOwnsCleaningResource,
    fetchUserOfferForCleaningJob,
    fetchAllOffersForCleaningJob,
    user,
  ]);

  if (isLoading) return <EuiLoadingSpinner size="xl" />;
  if (!currentCleaningJob) return <EuiLoadingSpinner size="xl" />;
  if (!currentCleaningJob?.name) return <NotFoundPage />;

  const editJobButton = userOwnsCleaningResource ? (
    <EuiButtonIcon
      iconType={"documentEdit"}
      aria-label="edit"
      onClick={() => navigate("edit")}
    />
  ) : null;

  const goBackButton = (
    <EuiButtonEmpty
      iconType={"sortLeft"}
      size="s"
      onClick={() => navigate(`/cleaning-jobs/${currentCleaningJob.id}`)}
    />
  );

  const viewCleaningJobElement = (
    <CleaningJobCard
      user={user}
      offersError={offersError}
      cleaningJob={currentCleaningJob}
      offersIsLoading={offersIsLoading}
      isOwner={userOwnsCleaningResource}
      createOfferForCleaning={createOfferForCleaning}
    />
  );

  const editCleaningJobElement = (
    <PermissionsNeeded
      element={<CleaningJobEditForm cleaningJob={currentCleaningJob} />}
      isAllowed={userOwnsCleaningResource}
    />
  );

  const cleaningJobOffersTableElement = userOwnsCleaningResource ? (
    <CleaningJobOffersTable
      offers={
        allOffersForCleaningJob ? Object.values(allOffersForCleaningJob) : []
      }
      offersIsUpdating={offersIsUpdating}
      offersIsLoading={offersIsLoading}
      handleAcceptOffer={acceptUsersOfferForCleaningJob}
    />
  ) : null;

  return (
    <StyledEuiPage>
      <EuiPageBody component="section">
        <EuiPageContent
          verticalPosition="center"
          horizontalPosition="center"
          // paddingSize="none"
        >
          <StyledFlexGroup justifyContent="flexStart" alignItems="center">
            <EuiFlexItem>
              <EuiFlexGroup
                justifyContent="flexStart"
                alignItems="center"
                direction="row"
                responsive={false}
              >
                <EuiFlexItem grow={false}>
                  <EuiAvatar
                    size="xl"
                    name={
                      currentCleaningJob.owner?.profile?.full_name ||
                      currentCleaningJob.owner?.username ||
                      "Anonymous"
                    }
                    initialsLength={2}
                    imageUrl={currentCleaningJob.owner?.profile?.image}
                  />
                </EuiFlexItem>
                <EuiFlexItem>
                  <EuiTitle>
                    <p>@{currentCleaningJob.owner?.username}</p>
                  </EuiTitle>
                </EuiFlexItem>
              </EuiFlexGroup>
            </EuiFlexItem>
            <EuiFlexItem grow={false}>
              <Routes>
                <Route path="/" element={editJobButton} />
                <Route path="/edit" element={goBackButton} />
              </Routes>
            </EuiFlexItem>
          </StyledFlexGroup>

          <EuiPageContentBody>
            <Routes>
              <Route path="/" element={viewCleaningJobElement} />
              <Route path="/edit" element={editCleaningJobElement} />
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </EuiPageContentBody>
        </EuiPageContent>
        <Routes>
          <Route path="/" element={cleaningJobOffersTableElement} />
        </Routes>
      </EuiPageBody>
    </StyledEuiPage>
  );
};

export default connect(
  (state) => ({
    user: state.auth.user,
    isLoading: state.cleanings.isLoading,
    cleaningError: state.cleanings.cleaningsError,
    currentCleaningJob: state.cleanings.currentCleaningJob,

    offersIsLoading: state.offers.isLoading,
    offersIsUpdating: state.offers.isUpdating,
    offersError: state.offers.error,
  }),
  {
    fetchCleaningJobById: cleaningActions.fetchCleaningJobById,
    clearCurrentCleaningJob: cleaningActions.clearCurrentCleaningJob,
    createOfferForCleaning: offersActions.createOfferForCleaning,
    fetchAllOffersForCleaningJob: offersActions.fetchAllOffersForCleaningJob,
    fetchUserOfferForCleaningJob: offersActions.fetchUserOfferForCleaningJob,
    acceptUsersOfferForCleaningJob:
      offersActions.acceptUsersOferrForCleaningJob,
  }
)(CleaningJobView);
