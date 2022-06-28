// eslint-disable-next-line
export default {
  auth: {
    isLoading: false,
    error: false,
    user: {},
  },
  cleanings: {
    isLoading: false,
    isUpdating: false,
    error: false,
    data: {},
    currentCleaningJob: null,
    activeCleaningId: null,
  },
  offers: {
    isLoading: false,
    isUpdating: false,
    error: false,
    data: {},
  },
  feed: {
    isLoading: false,
    error: null,
    data: {},
    hasNext: {},
  },
  ui: {
    toastList: [],
  },
};
