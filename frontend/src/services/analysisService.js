import api from "./api";

/**
 * Starts document analysis.
 * Returns immediately because the backend runs the analysis
 * in a BackgroundTask.
 */
export async function analyzeDocument(documentId) {
  const response = await api.post(
    `/documents/${documentId}/analyze`
  );

  return response.data;
}

/**
 * Fetches the completed analysis.
 * Throws an error if the analysis isn't ready yet.
 */
export async function getAnalysis(documentId) {
  const response = await api.get(
    `/documents/${documentId}/analysis`
  );

  return response.data;
}

/**
 * Polls until the analysis is ready.
 * Tries every 2 seconds.
 */
export async function waitForAnalysis(
  documentId,
  interval = 2000,
  maxAttempts = 30
) {
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      const analysis = await getAnalysis(documentId);
      return analysis;
    } catch (error) {
      // If analysis is still processing, wait and retry
      if (error.response?.status === 404) {
        await new Promise((resolve) =>
          setTimeout(resolve, interval)
        );
        continue;
      }

      // Any other error should be thrown
      throw error;
    }
  }

  throw new Error("Analysis timed out.");
}