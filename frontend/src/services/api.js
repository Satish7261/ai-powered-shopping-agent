const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8000";


export async function sendMessage(
  message,
  history = []
) {

  const formData = new FormData();

  formData.append(
    "message",
    message
  );

  formData.append(
    "history",
    JSON.stringify(history)
  );


  try {

    const response = await fetch(
      `${API_URL}/chat`,
      {
        method: "POST",
        body: formData,
      }
    );


    const data =
      await response.json();


    console.log(
      "CHAT API RESPONSE:",
      data
    );


    if (!response.ok) {

      throw new Error(
        data.response ||
        `Server error: ${response.status}`
      );

    }


    if (!data.success) {

      throw new Error(
        data.response ||
        "Shopping agent returned an error."
      );

    }


    return data;


  } catch (error) {

    console.error(
      "CHAT API ERROR:",
      error
    );

    throw error;

  }
}


export async function searchByImage(
  file
) {

  const formData = new FormData();

  formData.append(
    "file",
    file
  );


  try {

    const response = await fetch(
      `${API_URL}/image-search`,
      {
        method: "POST",
        body: formData,
      }
    );


    const data =
      await response.json();


    if (!response.ok) {

      throw new Error(
        data.response ||
        `Server error: ${response.status}`
      );

    }


    if (!data.success) {

      throw new Error(
        data.response ||
        "Image search failed."
      );

    }


    return data;


  } catch (error) {

    console.error(
      "IMAGE API ERROR:",
      error
    );

    throw error;

  }
}


export async function checkHealth() {

  const response = await fetch(
    `${API_URL}/health`
  );


  if (!response.ok) {

    throw new Error(
      "Backend is not healthy"
    );

  }


  return await response.json();
}