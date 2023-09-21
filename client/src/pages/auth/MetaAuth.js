export const initFacebookSdk = () => {
    return new Promise((resolve, reject) => {
        console.log('initializing facebook sdk')
        // Load the Facebook SDK asynchronously
        window.fbAsyncInit = () => {
            console.log('loading facebook sdk')
            window.FB.init({
                appId: '319135230864852',
                cookie: true,
                xfbml: true,
                version: 'v18.0'
            });

            // Resolve the promise when the SDK is loaded
            resolve();
        };
        console.log('facebook sdk loaded')
    })
}

export const getFacebookLoginStatus = () => {
    return new Promise((resolve, reject) => {
        window.FB.getLoginStatus((response) => {
            resolve(response);
        });
    });
};

export const fbLogin = () => {
    return new Promise((resolve, reject) => {
        window.FB.login((response) => {
            resolve(response)
        })
    })
}