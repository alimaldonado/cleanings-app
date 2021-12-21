import React, { useEffect } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import { connect } from "react-redux";
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
  createOfferForCleaning,
  fetchUserOfferForCleaningJob,
}) => {
  const { cleaning_id } = useParams();

  const navigate = useNavigate();

  const userOwnsCleaningResource =
    user?.username && currentCleaningJob?.owner?.id === user?.id;

  useEffect(() => {
    if (cleaning_id && user?.username) {
      fetchCleaningJobById({ cleaning_id });

      if (!userOwnsCleaningResource)
        fetchUserOfferForCleaningJob({ cleaning_id, username: user.username });
    }
    return () => clearCurrentCleaningJob();
  }, [
    cleaning_id,
    fetchCleaningJobById,
    clearCurrentCleaningJob,
    userOwnsCleaningResource,
    fetchUserOfferForCleaningJob,
    user,
  ]);

  if (isLoading) return <EuiLoadingSpinner size="xl" />;
  if (!currentCleaningJob) return <EuiLoadingSpinner size="xl" />;
  if (!currentCleaningJob?.name) return <NotFoundPage />;

  const userOwndCleaningResource = currentCleaningJob?.owner?.id === user?.id;

  const editJobButton = userOwndCleaningResource ? (
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
      isOwner={userOwndCleaningResource}
      createOfferForCleaning={createOfferForCleaning}
    />
  );

  const editCleaningJobElement = (
    <PermissionsNeeded
      element={<CleaningJobEditForm cleaningJob={currentCleaningJob} />}
      isAllowed={userOwndCleaningResource}
    />
  );
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
    offersError: state.offers.error,
  }),
  {
    fetchCleaningJobById: cleaningActions.fetchCleaningJobById,
    clearCurrentCleaningJob: cleaningActions.clearCurrentCleaningJob,

    createOfferForCleaning: offersActions.createOfferForCleaning,
    fetchUserOfferForCleaningJob: offersActions.fetchUserOfferForCleaningJob,
  }
)(CleaningJobView);
