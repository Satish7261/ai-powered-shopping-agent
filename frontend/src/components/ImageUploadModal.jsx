import {
    X,
    Upload,
    Image as ImageIcon,
    Sparkles,
} from "lucide-react";

import {
    useRef,
    useState,
} from "react";



function ImageUploadModal({
    onClose,
    onUpload,
    loading,
}) {


    const inputRef =
        useRef(null);


    const [
        preview,
        setPreview,
    ] = useState(null);


    const [
        selectedFile,
        setSelectedFile,
    ] = useState(null);



    /*
    |--------------------------------------------------------------------------
    | Handle selected image
    |--------------------------------------------------------------------------
    */

    const handleFile = (
        file
    ) => {

        if (!file) {

            return;

        }


        const allowedTypes = [

            "image/jpeg",

            "image/png",

            "image/webp",

        ];


        if (
            !allowedTypes.includes(
                file.type
            )
        ) {

            alert(
                "Please upload a JPG, PNG or WEBP image."
            );

            return;

        }


        setSelectedFile(
            file
        );


        setPreview(
            URL.createObjectURL(
                file
            )
        );

    };



    /*
    |--------------------------------------------------------------------------
    | Analyze image
    |--------------------------------------------------------------------------
    */

    const handleAnalyze = () => {

        if (
            !selectedFile
        ) {

            return;

        }


        onUpload(
            selectedFile
        );

    };



    return (

        <div
            className="modal-overlay"
            onMouseDown={(event) => {

                if (
                    event.target ===
                    event.currentTarget
                ) {

                    onClose();

                }

            }}
        >


            <div className="image-modal">


                {/* Close */}

                <button
                    className="modal-close"
                    onClick={onClose}
                    disabled={loading}
                >

                    <X
                        size={19}
                    />

                </button>



                {/* Icon */}

                <div className="modal-main-icon">

                    <ImageIcon
                        size={27}
                    />

                </div>



                {/* Heading */}

                <div className="modal-heading">

                    <h2>
                        Shop by Image
                    </h2>

                    <p>
                        Upload a product photo
                        and let AI find similar
                        products in the store.
                    </p>

                </div>



                {/* Upload */}

                {!preview ? (

                    <button
                        className="drop-zone"
                        onClick={() =>
                            inputRef.current?.click()
                        }
                    >

                        <div className="drop-icon">

                            <Upload
                                size={23}
                            />

                        </div>


                        <strong>
                            Upload a product image
                        </strong>


                        <span>
                            JPG, PNG or WEBP
                        </span>

                    </button>

                ) : (

                    <div className="preview-wrapper">

                        <img
                            src={preview}
                            alt="Product preview"
                        />


                        <button
                            className="change-image"
                            onClick={() =>
                                inputRef.current?.click()
                            }
                            disabled={loading}
                        >
                            Change image
                        </button>

                    </div>

                )}



                {/* Hidden file input */}

                <input
                    ref={inputRef}
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    hidden
                    onChange={(event) =>
                        handleFile(
                            event.target.files?.[0]
                        )
                    }
                />



                {/* Analyze button */}

                <button
                    className="analyze-button"
                    disabled={
                        !selectedFile ||
                        loading
                    }
                    onClick={
                        handleAnalyze
                    }
                >

                    <Sparkles
                        size={16}
                    />

                    {

                        loading

                            ? "Analyzing..."

                            : "Find Similar Products"

                    }

                </button>



                <p className="privacy-note">

                    Your image is used only
                    to identify similar products.

                </p>


            </div>

        </div>

    );

}


export default ImageUploadModal;