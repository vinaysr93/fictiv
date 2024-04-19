import streamlit as st

from PIL import Image
from fastbook import load_learner
import tempfile
import os
def overlay_image(image1,image2,alpha,x,y,rotation,re_size): 


    image1=Image.open(image1)

    image2=Image.open(image2)
    image2=image2.rotate(rotation)
    image2=image2.resize(re_size)

    trans=int(alpha*255)
    image2.putalpha(trans)

    image1.paste(image2,mask=image2,box=[x,y])
    return image1


def main_loop():
        

    
    base_file= st.file_uploader("Choose the base file")
    overlay_file=st.file_uploader("Choose the overlay file")
    if base_file and overlay_file:
        
        st.subheader("Original Images")
        st.image([base_file,overlay_file],width=300)
        base_file_size=Image.open(base_file).size
        overlay_file_size=Image.open(overlay_file).size
        st.write(base_file_size)
    
        st.sidebar.title('Settings')
    
    
        
        x_movement=st.sidebar.slider("X Movement",min_value=0,max_value=base_file_size[0],step=1,value=0)
        y_movement=st.sidebar.slider("Y Movement",min_value=0,max_value=base_file_size[1],step=1,value=0)
        rotate_degree=st.sidebar.slider("Rotation",min_value=-180,max_value=180,step=1,value=0)
        resize_x=st.sidebar.slider("Resize in X",min_value=0,max_value=base_file_size[0],step=1,value=overlay_file_size[0])
        resize_y=st.sidebar.slider("Resize in Y",min_value=0,max_value=base_file_size[1],step=1,value=overlay_file_size[1])
        alpha = st.sidebar.slider('Overlay Transparency', min_value=0.0, max_value=1.0,step= 0.01)
        
    
    
    #position=st.sidebar.slider("X axis oritntation",min)
    blended_image=None
    if base_file is not None and overlay_file is not None:
        blended_image=overlay_image(base_file,overlay_file,alpha,x_movement,y_movement,rotate_degree,[resize_x,resize_y])

    if blended_image:
        st.image(blended_image,caption="Overlay Image",use_column_width=True)



    st.divider()

    learn_inf = load_learner('model.pkl')  
    st.subheader("Predicting ano color from an Image (Red,Blue,Black,Green)")
    pred_file = st.file_uploader("Choose the file to detect ano color")
    if pred_file:
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, pred_file.name)
        with open(path, "wb") as f:
            f.write(pred_file.read())    
    
        st.image(pred_file,width=300)
        
        pred,pred_idx,probs=learn_inf.predict(path)
        st.text(f" The anodizing color is {pred} and probability is {probs[pred_idx]:.04f}")


if __name__=='__main__':

    main_loop()
