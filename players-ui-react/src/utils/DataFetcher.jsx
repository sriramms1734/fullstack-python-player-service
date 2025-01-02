export default async function fetchData(ep) {
    const endpoint = ep || '/v1/players'
    return fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            return data;
        }).catch(error => {
            console.log('oops there was an error', error)
    })
};

export async function fetchPostData() {
    const endpoint = 'http://127.0.0.1:5300/team/generate';
    return fetch(endpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"seed_id": "abbotji01", "team_size": 10})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        return data;
    })
    .catch(error => {
        console.log('oops there was an error', error);
    });
};