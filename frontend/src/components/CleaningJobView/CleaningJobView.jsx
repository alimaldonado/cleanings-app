import React from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import {
  EuiPage,
  EuiPageBody,
  EuiPageContent,
  EuiPageContentBody,
  EuiLoadingSpinner,
  EuiFlexGroup,
  EuiFlexItem,
  EuiTitle,
  EuiButtonIcon,
  EuiButtonEmpty,
} from "@elastic/eui";
import { useParams } from "react-router-dom";
import styled from "styled-components";
import {
  CleaningJobCard,
  CleaningJobEditForm,
  NotFoundPage,
  PermissionsNeeded,
  CleaningJobOffersTable,
  UseAvatar,
} from "components";
import { useSingleCleaningJob } from "hooks/cleanings/useSingleCleaningJob";

const StyledEuiPage = styled(EuiPage)`
  flex: 1;
`;

const StyledFlexGroup = styled(EuiFlexGroup)`
  padding: 1rem;
`;

const CleaningJobView = () => {
  const { cleaningId } = useParams();
  const navigate = useNavigate();
  const {
    cleaningJob,
    // error,
    isLoading,
    // isUpdating,
    activeCleaningId,
    userIsOwner,
  } = useSingleCleaningJob(cleaningId);

  if (isLoading) return <EuiLoadingSpinner size="xl" />;
  if (!cleaningJob && activeCleaningId !== cleaningId) return <NotFoundPage />;

  const editJobButton = userIsOwner ? (
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
      onClick={() => navigate(`/cleaning-jobs/${cleaningJob.id}`)}
    />
  );

  const viewCleaningJobElement = (
    <CleaningJobCard
      offersIsLoading={null}
      cleaningJob={cleaningJob}
      isOwner={userIsOwner}
      createOfferForCleaning={null}
      userOfferForCleaningJob={null}
    />
  );

  const editCleaningJobElement = (
    <PermissionsNeeded
      element={<CleaningJobEditForm cleaningId={cleaningId} />}
      isAllowed={userIsOwner}
    />
  );

  const cleaningJobOffersTableElement = userIsOwner ? (
    <CleaningJobOffersTable
      offers={[]}
      offersIsLoading={null}
      handleAcceptOffer={null}
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
                  <UseAvatar
                    size="xl"
                    user={cleaningJob.owner}
                    initialsLength={2}
                  />
                </EuiFlexItem>
                <EuiFlexItem>
                  <EuiTitle>
                    <p>@{cleaningJob.owner?.username}</p>
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

export default CleaningJobView;
