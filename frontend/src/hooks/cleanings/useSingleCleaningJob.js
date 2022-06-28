import { useAuthenticatedUser } from "hooks/auth/useAuthenticatedUser";
import { useEffect } from "react";
import { shallowEqual } from "react-redux";
import { useDispatch, useSelector } from "react-redux";
import { userIsOwnerOfCleaningJob } from "utils/cleanings";
import { Actions as cleaningActions } from "redux/cleanings";

export const useSingleCleaningJob = (cleaningId) => {
  const dispatch = useDispatch();
  const { user } = useAuthenticatedUser();
  const cleaningJob = useSelector(
    (state) => state.cleanings.data[cleaningId],
    shallowEqual
  );
  const activeCleaningId = useSelector(
    (state) => state.cleanings.activeCleaningId
  );
  const isLoading = useSelector((state) => state.cleanings.isLoading);
  const isUpdating = useSelector((state) => state.cleanings.isUpdating);
  const error = useSelector((state) => state.cleanings.error, shallowEqual);
  const userIsOwner = userIsOwnerOfCleaningJob(cleaningJob, user);

  useEffect(() => {
    if (cleaningId && !cleaningJob) {
      dispatch(cleaningActions.fetchCleaningJobById({ cleaningId }));
    }

    return () => {
      dispatch(cleaningActions.clearCurrentCleaningJob());
    };
  }, [dispatch, cleaningId, cleaningJob]);

  return {
    error,
    isLoading,
    isUpdating,
    cleaningJob,
    userIsOwner,
    activeCleaningId,
  };
};
