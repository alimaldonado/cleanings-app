import { combineReducers } from "redux";
import authReducer from "./auth";
import cleaningsReducer from "./cleanings";
import offersReducer from "./offers";
import feedReducer from "./feed";

const rootReducer = combineReducers({
  auth: authReducer,
  cleanings: cleaningsReducer,
  offers: offersReducer,
  feed: feedReducer,
});

export default rootReducer;
