/**
 * Formats API requests URLs
 *
 * @param {String} base - url string representing api endpoint without query params
 * @param {Object} params - query params to format and append to end of url
 */
export const formatURLWithQueryParams = (base, params) => {
  if (!params || Object.keys(params)?.length === 0) return base;

  const query = Object.entries(params)
    .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
    .join("&");

  return `${base}?${query}`;
};

/**
 * Format API request paths
 *
 * @param {String} path - relavite path to api endpoint
 */
export const formatAPIPath = (path) => {
  let adjustedPath = path;

  if (adjustedPath.charAt(0) !== "/") {
    adjustedPath = "/" + adjustedPath;
  }
  if (adjustedPath.charAt(adjustedPath.length - 1) !== "/") {
    adjustedPath = adjustedPath + "/";
  }
  return adjustedPath;
};

/**
 * Formats API requests URLs
 *
 * @param {String} url - url string representing relative path to api endpoint
 * @param {Object} params - query params to format at end of url
 */
export const formatURL = (url, params) => {
  const endpointPath = formatAPIPath(url);

  const baseUrl =
    process.env.NODE_ENV === "production"
      ? process.env.REMOVE_SERVER_URL
      : "http://localhost:5500/api";

  const fullURL = `${baseUrl}${endpointPath}`;

  return formatURLWithQueryParams(fullURL, params);
};
