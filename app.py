import streamlit as st
import cv2
import numpy as np

from scanner.detection import (
    find_page,
    get_debug_images
)

from scanner.perspective import (
    warp_page
)

from scanner.thresholding import (
    binarize
)


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Document Scanner",
    page_icon="📄",
    layout="centered"
)


# --------------------------------------------------
# UI
# --------------------------------------------------

st.title("📄 Classic Computer Vision Scanner")

st.write(
    "Upload a photo of a receipt or printed page."
)


uploaded_file = st.file_uploader(
    "Choose an image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


# --------------------------------------------------
# Image uploaded
# --------------------------------------------------

if uploaded_file is not None:

    # Read uploaded file
    file_bytes = np.asarray(
        bytearray(
            uploaded_file.read()
        ),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    if image is None:

        st.error(
            "Could not read the uploaded image."
        )

        st.stop()

    # --------------------------------------------------
    # Original
    # --------------------------------------------------

    st.subheader("1. Original")

    st.image(
        cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        ),
        use_container_width=True
    )

    # --------------------------------------------------
    # Debug images
    # --------------------------------------------------

    debug = get_debug_images(
        image
    )

    with st.expander(
        "🔍 Show computer-vision debug images"
    ):

        col1, col2 = st.columns(2)

        with col1:

            st.write("Grayscale")

            st.image(
                debug["gray"],
                use_container_width=True
            )

            st.write("Adaptive Threshold")

            st.image(
                debug["adaptive"],
                use_container_width=True
            )

        with col2:

            st.write("Canny Edges")

            st.image(
                debug["edges"],
                use_container_width=True
            )

            st.write("Otsu Threshold")

            st.image(
                debug["otsu"],
                use_container_width=True
            )

    # --------------------------------------------------
    # Detect page
    # --------------------------------------------------

    try:

        corners = find_page(
            image
        )

        # --------------------------------------------------
        # Show detected corners
        # --------------------------------------------------

        debug_image = image.copy()

        cv2.polylines(
            debug_image,
            [
                corners.astype(
                    np.int32
                )
            ],
            True,
            (0, 255, 0),
            5
        )

        for point in corners:

            x, y = point.astype(
                np.int32
            )

            cv2.circle(
                debug_image,
                (x, y),
                12,
                (0, 0, 255),
                -1
            )

        st.subheader(
            "2. Detected Page"
        )

        st.image(
            cv2.cvtColor(
                debug_image,
                cv2.COLOR_BGR2RGB
            ),
            use_container_width=True
        )

        # --------------------------------------------------
        # Perspective correction
        # --------------------------------------------------

        warped = warp_page(
            image,
            corners
        )

        st.subheader(
            "3. Perspective Corrected"
        )

        st.image(
            cv2.cvtColor(
                warped,
                cv2.COLOR_BGR2RGB
            ),
            use_container_width=True
        )

        # --------------------------------------------------
        # Binarization
        # --------------------------------------------------

        scanned = binarize(
            warped
        )

        st.subheader(
            "4. Final Scan"
        )

        st.image(
            scanned,
            use_container_width=True
        )

        # --------------------------------------------------
        # Download
        # --------------------------------------------------

        success, encoded = cv2.imencode(
            ".png",
            scanned
        )

        if success:

            st.download_button(
                label="⬇️ Download Scan",
                data=encoded.tobytes(),
                file_name="scanned_document.png",
                mime="image/png"
            )

    except Exception as error:

        st.error(
            f"Could not detect the document: {error}"
        )

        st.warning(
            "Open the debug section above. "
            "It shows exactly what OpenCV sees."
        )
