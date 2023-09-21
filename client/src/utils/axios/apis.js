import instance from "./conf";

const apis = {
    login: async (data) => {
        return await instance.post("users/login/" , data);
    },
    is_authenticated: async () => {
        return await instance.get("users/is-authenticated/");
    },
    post_code: async (data) => {
        return await instance.post("users/exchange_code_for_token/", data);
    },
    get_calendar_events: async () => {
        return await instance.get("users/events/");
    },
    google_login: async (data) => {
        return await instance.post("users/google-login/", data);
    }
};

export default apis;
