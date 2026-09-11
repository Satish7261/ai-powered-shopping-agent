import {
    Sparkles,
    LoaderCircle,
} from "lucide-react";



function TypingIndicator() {

    return (

        <div className="message-row">


            <div className="avatar ai-avatar">

                <Sparkles
                    size={16}
                />

            </div>


            <div className="typing-bubble">

                <LoaderCircle
                    size={16}
                    className="spin"
                />

                <span>
                    ShopAI is thinking...
                </span>

            </div>


        </div>

    );

}


export default TypingIndicator;