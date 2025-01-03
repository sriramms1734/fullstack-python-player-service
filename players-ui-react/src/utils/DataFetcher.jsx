export default async function fetchData(ep) {
    const endpoint = ep || '/v1/players'
    try {
        const response = await fetch(endpoint);
        return response.json();
    } catch(error) {
        console.log('oops there was an error', error)
    }
};

export async function postData(bodyInput) {
    const endpoint = 'http://localhost:11434/team/generate';
    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(bodyInput)
        })
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const result = await response.json();
        return result;
    } catch(error){
        console.log('oops there was an error', error);
    }
};