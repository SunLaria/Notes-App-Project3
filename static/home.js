const root = ReactDOM.createRoot(document.getElementById('root'));

const user_id = document.getElementById("user-id").innerText;

function Note(p) {
    const [text, setText] = React.useState(p.text);
    const [id, setId] = React.useState(p.id);
    const [edit, setEdit] = React.useState(false);

    const changeEvent = (e) => {
        e.stopPropagation();
        const newText = e.target.value;
        setText(newText);
        if (text !== newText) {
            axios.patch('/api/note', { note_id: id, text: newText })
                .then((response) => {
                    response.data['result'] == `Note ${id} Updated` ?
                        console.log(`Note ${id}, Text Updated: ${newText}`) :
                        console.log('Failed to update the Note');
                })
                .catch((error) => {console.error('Error updating note:', error)});
        }
    };

    const deleteEvent = (e) => {
        e.stopPropagation();
        axios.delete('/api/note',{params:{note_id:id}})
            .then((response) => {
                if (response.data['result'].includes("Deleted")) {
                    console.log(`Note ${id} Deleted`);
                    e.target.parentElement.parentElement.remove();
                } else {
                    console.log(`Note ${id} Failed To Delete`);
                }
            })
            .catch((error) => {console.error('Error deleting note:', error)});
    };

    return (
        <div>
            <div className="note-card" onMouseEnter={() => setEdit(true)} onMouseLeave={() => setEdit(false)}>
                <textarea
                    defaultValue={text}
                    onDoubleClick={(e) => deleteEvent(e)}
                    id={id}
                    onChange={(e) => changeEvent(e)}
                />
                {edit ? <NoteDateInfo created={p.created} /> : ""}
            </div>
        </div>
    );
}

function NoteDateInfo(p) {
    return (
        <div className="note-date-info">
            <div className="date-divs">
                <div className="date-div">Created: {p.created}</div>
            </div>
        </div>
    );
}

function Notes() {
    const [userNotes, setUserNotes] = React.useState([]);

    React.useEffect(() => {
        axios.get(`/api/note?user_id=${user_id}`)
            .then((response) => {
                setUserNotes(response.data);
                console.log(response.data);
            })
            .catch((error) => {console.error('Error fetching user notes:', error)});
    }, []);

    const addEmptyNote = () => {
        let date = new Date();
        axios.post('/api/note', { text: "", user_id: user_id })
            .then((response) => {
                const newNoteId = response.data.result.split("Note Created With id ")[1];
                setUserNotes([...userNotes, { id: newNoteId, text: '', user: user_id, created_at:date.toISOString().slice(0, 10)}]);
                console.log(`Note Created with id ${newNoteId}`);
            })
            .catch((error) => {console.error('Error creating note:', error)});
    };

    return (
        <div id="content" onDoubleClick={() => addEmptyNote()}>
            <div id="user-notes" >
                {userNotes.map((i) => {
                    return <Note text={i.text} id={i.id} key={i.id} created={i.created_at} />;
                })}
            </div>
        </div>
    );
}

root.render(<Notes />);
