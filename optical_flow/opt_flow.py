import cv2
import numpy as np
import os

def draw_flow(img, flow, file_name, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = img.copy() #cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    cv2.imwrite(file_name, vis)

def improve_segmentation(prev_seg, curr_seg, flow, file_name, step=1):
    h, w = prev_seg.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    #lines = np.int32(lines + 0.5)
    new_seg = curr_seg.copy()
    pixel_size = 1
    #cv2.polylines(new_seg, lines, 0, (0, 255, 0))
    for (x1, y1), (x2, y2) in lines:
        pts1 = (int(x2), int(y2))
        pts2 = (int(x2) + pixel_size, int(y2) + pixel_size)
        color = tuple(prev_seg[int(y1), int(x1)].astype(np.int))
        #cv2.circle(new_seg, (x1, y1), 1, (0, 255, 0), -1)
        cv2.circle(new_seg, pts1, pixel_size, color, -1)
    kernel = (15, 15)
    #new_seg = cv2.morphologyEx(new_seg, cv2.MORPH_CLOSE, kernel)
    #new_seg = cv2.medianBlur(new_seg, 9)
    cv2.imwrite(file_name, new_seg)

if __name__ == "__main__":
    directory= "."
    sources_dir = os.path.join(directory, "src")
    segmentations_dir = os.path.join(directory, "seg")
    output_dir = os.path.join(directory, "out")
    prev_gray = None
    prev_seg = None

    for i, (src, seg) in enumerate(zip(sorted(os.listdir(sources_dir)), sorted(os.listdir(segmentations_dir)))):
        src_path = os.path.join(sources_dir, src)
        seg_path = os.path.join(segmentations_dir, seg)
        gray = cv2.imread(src_path, 0)
        seg_img = cv2.imread(seg_path, 1)

        print(src, seg, i)
        if i < 1:
            prev_gray = gray
            continue

        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        prev_gray = gray
        prev_seg = seg_img

        file_name = os.path.join(output_dir, src)
        improve_segmentation(prev_seg, seg_img, flow, file_name)
        file_name = os.path.join(output_dir, "flow_" + src)
        draw_flow(seg_img, flow, file_name)