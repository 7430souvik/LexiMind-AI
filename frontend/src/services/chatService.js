import api from "./api";

export async function askQuestion(
  documentId,
  question
) {
  const response = await api.post(
    `/documents/${documentId}/chat`,
    {
      question,
    }
  );

  return response.data;
}