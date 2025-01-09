async function authenticate() {
    if (!window.ethereum) {
        alert("Please install a wallet like MetaMask.");
        return;
    }

    const web3 = new Web3(window.ethereum);
    await window.ethereum.request({ method: 'eth_requestAccounts' });
    const accounts = await web3.eth.getAccounts();
    const userAddress = accounts[0];

    const response = await fetch('/get_nonce/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address: userAddress })
    });


    const responseData = await response.json();
    if (responseData.error) {
        console.error("Error fetching nonce:", responseData.error);
        return;
    }

    const nonce = responseData.nonce;
    const signature = await web3.eth.personal.sign(nonce, userAddress, '');

    const verificationResponse = await fetch('/verify_signature/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address: userAddress, signature: signature })
    });

    const result = await verificationResponse.json();
    if (result.success) {
        console.log("Authentication successful");
        localStorage.setItem('auth_token', result.access_token);
        window.location.href = '/home';
    } else {
        console.error("Authentication failed:", result.error);
    }
}

document.getElementById('wallet-login-btn').addEventListener('click', authenticate);
