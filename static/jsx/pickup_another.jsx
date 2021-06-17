'use strict';

function PickingUpForAnother() {
    function alertMessage() {
        alert('You clicked yes');
    }

    function handleSubmit(evt) {
        const householdInfo = {
            'num-people': $('#num-people').val(),
            'wants-peanut-butter': $('#wants-peanut-butter').val(),
            'picking-up-for-another': $('#picking-up-for-another').val(),
            'allergies': $('#allergies'),
            'special-requests': $('#special-requests')
        }

        $.post('/handle-household-info', householdInfo)
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type="number" id="num-people" required></input>
                <label>Number of people in household</label><br></br>
                <label>Would you like peanut butter?</label>
                <input type="radio" id="wants-peanut-butter"  value="True"></input>
                <label>Yes</label>
                <input type="radio" id="wants-peanut-butter" value="False"></input><br></br>
                <label>Are you picking up for anyone else?</label>
                <input onClick={alertMessage} type="radio" id="picking-up-for-another" value="True"></input>
                <label>Yes</label>
                <input type="radio" id="picking-up-for-another" value="False"></input>
                <label>No</label><br></br>
                <input type="text" id="allergies"></input>
                <label>Allergies</label><br></br>
                <input type="text" id="special-requests"></input>
                <label>Any special requests?</label><br></br>
                <input type="submit" name="submit"></input>
            </form>
        </div>
    );
}

ReactDOM.render(
    <PickingUpForAnother />,
    document.querySelector('#household-info')
)

