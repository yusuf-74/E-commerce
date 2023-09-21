
import axios from "axios";

export const baseURL = "http://localhost/api/v1/";
// export const baseURL = "staging";
// export const baseURL = "production";

const instance = axios.create({
    baseURL,
    headers: {
        Accept: "application/json",
        Authorization: localStorage.getItem("access_token")
            ? "Bearer " + localStorage.getItem("access_token")
            : null,
    },
});

instance.interceptors.request.use((config) => {
    const accessToken = localStorage.getItem("access_token")
        ? "Bearer " + localStorage.getItem("access_token")
        : null;
        config.headers["Authorization"] = accessToken;
    return config;
});

instance.interceptors.response.use(
    (response) => {
        return response;
    },
    async (error) => {
        //Bearer token logic
        const originalRequest = error.config;

        if (
            error.response.status === 401 &&
            originalRequest.url === "users/refresh/"
        ) {
            return Promise.reject(error);
        }
        if (
            error.response.data.code === "token_not_valid" &&
            error.response.status === 401
        ) {
            const refreshToken = localStorage.getItem("refresh_token");

            if (refreshToken) {
                return instance
                    .post("users/refresh/", { refresh: refreshToken })
                    .then((response) => {
                        localStorage.setItem("access_token", response.data.access);
                        instance.defaults.headers["Authorization"] =
                            "Bearer " + response.data.access;
                        originalRequest.headers["Authorization"] =
                            "Bearer " + response.data.access;
                        return instance(originalRequest);
                    })
                    .catch((err) => { 
                        console.log(err)
                    });
            }
        }
        return Promise.reject(error);
    }
);

export default instance;