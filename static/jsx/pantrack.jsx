'use strict';

function Welcome() {
    return (
        <div>
            <h1>Welcome to PanTrack</h1>
        </div>
    );
}

function PickingUpForAnother() {
    // function alertMessage() {
    //     alert('Radio button has changed');
    // }


    return (
        <div>
            <h1>Hello</h1>
        </div>
    );
    // return (
    //     <button onClick={alertMessage}>
    //         Click me
    //     </button>
    // );
    // return (
    //     <div>
    //         <input type="radio" name="picking-up-for-another" value="True"></input>
    //         <label>Yes</label>
    //         <input type="radio" name="picking-up-for-another" value="False"></input>
    //         <label>No</label>
    //     </div>
    // );
}

ReactDOM.render(
    <PickingUpForAnother />,
    document.querySelector('#pickup')
)
ReactDOM.render(
    <Welcome />,
    document.querySelector('#welcome')
)

