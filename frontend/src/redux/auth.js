import initialState from "./initialState";
import axios from "axios";
import apiClient from "../services/apiClient";
import { Actions as cleaningActions } from "./cleanings";

export const REQUEST_LOGIN = "@@auth/REQUEST_LOGIN";
export const REQUEST_LOGIN_FAILURE = "@@auth/REQUEST_LOGIN_FAILURE";
export const REQUEST_LOGIN_SUCCESS = "@@auth/REQUEST_LOGIN_SUCCESS";
export const REQUEST_LOG_USER_OUT = "@@auth/REQUEST_LOG_USER_OUT";

export const FETCHING_USER_FROM_TOKEN = "@@auth/FETCHING_USER_FROM_TOKEN";
export const FETCHING_USER_FROM_TOKEN_SUCCESS =
  "@@auth/FETCHING_USER_FROM_TOKEN_SUCCESS";
export const FETCHING_USER_FROM_TOKEN_FAILURE =
  "@@auth/FETCHING_USER_FROM_TOKEN_FAILURE";

export const REQUEST_USER_SIGN_UP = "@@auth/REQUEST_USER_SIGN_UP";
export const REQUEST_USER_SIGN_UP_SUCCESS =
  "@@auth/REQUEST_USER_SIGN_UP_SUCCESS";
export const REQUEST_USER_SIGN_UP_FAILURE =
  "@@auth/REQUEST_USER_SIGN_UP_FAILURE";

export default function authReducer(state = initialState.auth, action = {}) {
  switch (action.type) {
    case REQUEST_LOGIN:
      return {
        ...state,
        isLoading: true,
      };

    case REQUEST_LOGIN_FAILURE:
      return {
        ...state,
        isLoading: false,
        error: action.error,
        user: {},
      };
    case REQUEST_LOGIN_SUCCESS:
      return {
        ...state,
        isLoading: false,
        error: null,
      };
    case REQUEST_LOG_USER_OUT:
      return {
        ...initialState.auth,
      };
    case FETCHING_USER_FROM_TOKEN:
      return {
        ...state,
        isLoading: true,
      };
    case FETCHING_USER_FROM_TOKEN_SUCCESS:
      return {
        ...state,
        isAuthenticated: true,
        userLoaded: true,
        isLoading: false,
        user: action.data,
      };
    case FETCHING_USER_FROM_TOKEN_FAILURE:
      return {
        ...state,
        isAuthenticated: false,
        userLoaded: true,
        isLoading: false,
        user: {},
      };
    case REQUEST_USER_SIGN_UP:
      return {
        ...state,
        isLoading: true,
      };
    case REQUEST_USER_SIGN_UP_SUCCESS:
      return {
        ...state,
        isLoading: false,
        error: null,
      };
    case REQUEST_USER_SIGN_UP_FAILURE:
      return {
        ...state,
        isLoading: false,
        isAuthenticated: false,
        error: action.error,
      };
    default:
      return state;
  }
}

export const Actions = {};

Actions.requestUserLogin = ({ email, password }) => {
  return async (dispatch) => {
    dispatch({ type: REQUEST_LOGIN });

    const formData = new FormData();

    formData.set("username", email);
    formData.set("password", password);

    const headers = {
      "Content-Type": "application/x-www-form-urlencoded",
    };

    try {
      const response = await axios({
        method: "POST",
        url: `http://localhost:5500/api/users/login/token/`,
        data: formData,
        headers,
      });

      console.log(response);

      const access_token = response?.data?.access_token;

      localStorage.setItem("access_token", access_token);

      dispatch({ type: REQUEST_LOGIN_SUCCESS });

      return dispatch(Actions.fetchUserFromToken(access_token));
    } catch (error) {
      console.log(error);

      return dispatch({
        type: REQUEST_LOGIN_FAILURE,
        error: error?.message,
      });
    }
  };
};

Actions.fetchUserFromToken = () => {
  return (dispatch) => {
    return dispatch(
      apiClient({
        url: `/users/me/`,
        method: `GET`,
        types: {
          REQUEST: FETCHING_USER_FROM_TOKEN,
          SUCCESS: FETCHING_USER_FROM_TOKEN_SUCCESS,
          FAILURE: FETCHING_USER_FROM_TOKEN_FAILURE,
        },
        options: {
          data: {},
          params: {},
        },
        onSuccess: (res) => {
          dispatch(cleaningActions.fetchAllUserOwnedCleaningJobs());
          return { success: true, status: res.status, data: res.data };
        },
      })
    );
  };
};

Actions.logUserOut = () => {
  localStorage.removeItem("access_token");
  return { type: REQUEST_LOG_USER_OUT };
};

Actions.registerNewUser = ({ username, email, password }) => {
  return (dispatch) =>
    dispatch(
      apiClient({
        url: `/users/`,
        method: `POST`,
        types: {
          REQUEST: REQUEST_USER_SIGN_UP,
          SUCCESS: REQUEST_USER_SIGN_UP_SUCCESS,
          FAILURE: REQUEST_USER_SIGN_UP_FAILURE,
        },
        options: {
          data: { username, email, password },
          params: {},
        },
        onSuccess: (response) => {
          const access_token = response?.data?.access_token?.access_token;

          localStorage.setItem("access_token", access_token);

          return dispatch(Actions.fetchUserFromToken(access_token));
        },
        onFailure: (response) => ({
          type: response.type,
          success: false,
          status: response.status,
          error: response.error,
        }),
      })
    );
};
