import gdsfactory as gf
import numpy as np

from jtwpa_design.tech import LAYER, Layer

from .rectangle import rectangle


PRINCETON_JJ_INITIAL_ROTATION = 135.0


def _JJ_feet(width: float, height: float, layer: Layer) -> gf.Component:
    c = gf.Component()
    pts = [
        (-width / 2, -height / 2),
        (width / 2, -height / 2),
        (width / 2, height / 2),
        (-width / 2, height / 2),
    ]
    c.add_polygon(pts, layer=layer)
    c.add_port(
        "top_right", center=(width / 2 - 0.5, height / 2), orientation=90, width=1, layer=layer
    )
    c.add_port(
        "top_left", center=(-width / 2 + 0.5, height / 2), orientation=90, width=1, layer=layer
    )
    c.add_port(
        "bottom_right", center=(width / 2 - 0.5, -height / 2), orientation=270, width=1, layer=layer
    )
    c.add_port(
        "bottom_left", center=(-width / 2 + 0.5, -height / 2), orientation=270, width=1, layer=layer
    )
    return c


@gf.cell()
def JJ1(
    width: float = 1.0,
    length: float = 8.0,
    feet_width_L: float = 6,
    feet_width_R: float = 6,
    feet_height: float = 3,
    extend_L: bool = False,
    extend_R: bool = False,
) -> gf.Component:
    c = gf.Component()

    if extend_L:
        JJ_1 = c << rectangle(width=width, height=length + 1, layer=LAYER.JJ)
        JJ_1.move((0, -((length + 1) / 2 - 2.5 - width / 2)))
    else:
        JJ_1 = c << rectangle(width=width, height=length, layer=LAYER.JJ)
        JJ_1.move((0, -(length / 2 - 2.5 - width / 2)))
    if extend_R:
        JJ_2 = c << rectangle(width=length + 1, height=width, layer=LAYER.JJ)
        JJ_2.move(((length + 1) / 2 - 2.5 - width / 2, 0))
    else:
        JJ_2 = c << rectangle(width=length, height=width, layer=LAYER.JJ)
        JJ_2.move((length / 2 - 2.5 - width / 2, 0))
    extend_1 = c << _JJ_feet(width=feet_width_R, height=feet_height, layer=LAYER.JJ)
    extend_2 = c << _JJ_feet(width=feet_width_L, height=feet_height, layer=LAYER.JJ)

    JJ_1.rotate(-45)
    JJ_2.rotate(-45)
    extend_1.connect("top_right", JJ_1.ports["bottom"])
    extend_2.connect("top_left", JJ_2.ports["right"])
    c.flatten()

    return c


@gf.cell()
def JJ2(
    width: float = 1.0,
    length: float = 8.0,
    feet_width_L: float = 6,
    feet_width_R: float = 6,
    feet_height: float = 3,
    extend_L: bool = False,
    extend_R: bool = False,
):
    c = gf.Component()

    if extend_R:
        JJ_1 = c << rectangle(width=width, height=length + 1, layer=LAYER.JJ)
        JJ_1.move((0, -((length + 1) / 2 - 2.5 - width / 2)))
    else:
        JJ_1 = c << rectangle(width=width, height=length, layer=LAYER.JJ)
        JJ_1.move((0, -(length / 2 - 2.5 - width / 2)))
    if extend_L:
        JJ_2 = c << rectangle(width=length + 1, height=width, layer=LAYER.JJ)
        JJ_2.move((-((length + 1) / 2 - 2.5 - width / 2), 0))
    else:
        JJ_2 = c << rectangle(width=length, height=width, layer=LAYER.JJ)
        JJ_2.move((-(length / 2 - 2.5 - width / 2), 0))
    extend_1 = c << _JJ_feet(width=feet_width_R, height=feet_height, layer=LAYER.JJ)
    extend_2 = c << _JJ_feet(width=feet_width_L, height=feet_height, layer=LAYER.JJ)

    JJ_1.rotate(-45)
    JJ_2.rotate(-45)
    extend_1.connect("top_left", JJ_1.ports["bottom"])
    extend_2.connect("top_right", JJ_2.ports["left"])
    c.flatten()

    return c


@gf.cell()
def create_jj_cross_princeton(
    jj_wid: float = 0.1,
    jj_len: float = 5,
    jj_arm_ext: float = 1,
    jj_shadow_len: float = 0.5,
    jj_arm_shadow_overlap: float = 0.1,
    comp_name: str = "jj_manha_princeton",
    layer_jj: Layer = LAYER.JJ,
    layer_jj_shadow: Layer = LAYER.JJ,
    layer_patches: Layer = LAYER.JJ,
    layer_patches_shadow: Layer = LAYER.JJ,
    merge_jj_and_patches: bool = True,
    pad_style: str = "rounded",
    square_size: float = 2.2,
    square_offset_x: float = 0.0,
    square_offset_y: float = 0.0,
    junction_arm_len_x: float = 0.0,
    junction_arm_len_y: float = 0.0,
    pad_connection_overlap: float = 0.75,
    square_connection_overlap: float = 0.15,
) -> gf.Component:
    """Creates the Princeton-style JJ cross.

    The source geometry distinguishes QEB main, shadow, patch, and patch shadow
    layers. This repo currently maps all four to ``LAYER.JJ``.
    """
    jj_arm1_wid = jj_wid + 0.02
    jj_arm1_len = jj_len

    jj_arm2_wid = jj_wid
    jj_arm2_len = jj_len

    jj_princeton = gf.Component()
    jj_cross = gf.Component()
    jj_patches = gf.Component()
    jj_patches_shadow = gf.Component()
    jj_princeton_jj = gf.Component()
    jj_princeton_shadow = gf.Component()

    jj_arm1_ref = jj_cross << gf.components.rectangle(size=(jj_arm1_wid, jj_arm1_len), layer=layer_jj)
    jj_arm2_ref = jj_cross << gf.components.rectangle(size=(jj_arm2_wid, jj_arm2_len), layer=layer_jj)
    jj_arm1_ref.rotate(angle=0)
    jj_arm1_ref.move((1, 0))

    jj_arm2_ref.rotate(angle=-90)
    jj_arm2_ref.move((0, 1 + jj_arm2_wid))

    for ref in [jj_arm1_ref, jj_arm2_ref]:
        ref.move((-jj_arm_ext - jj_arm1_wid / 2, -jj_arm_ext - jj_arm2_wid / 2))
        ref.rotate(angle=-45)

    jj_cross_ref = jj_princeton_jj << jj_cross
    jj_cross_ref.rotate(angle=135)

    patch_wid = 4
    patch_offset = 2
    patch_len = 6 + patch_offset
    patch_overlap = 0.6
    patch_shadow_wid = patch_wid + 1
    patch_shadow_len = patch_len + 1

    jj_patch_coord = np.array(
        [
            [-patch_wid / 2, -patch_len / 2],
            [patch_wid / 2, -patch_len / 2],
            [patch_wid / 2, patch_len / 2],
            [-patch_wid / 2, patch_len / 2],
        ]
    )
    jj_patch_shadow_coord = np.array(
        [
            [-patch_shadow_wid / 2, -patch_shadow_len / 2],
            [patch_shadow_wid / 2, -patch_shadow_len / 2],
            [patch_shadow_wid / 2, patch_shadow_len / 2],
            [-patch_shadow_wid / 2, patch_shadow_len / 2],
        ]
    )

    if pad_style not in {"rounded", "rectangle"}:
        raise ValueError(f"Unsupported pad_style: {pad_style}")

    jj_patches.add_polygon(jj_patch_coord, layer=layer_patches)
    jj_patches_shadow.add_polygon(jj_patch_shadow_coord, layer=layer_patches_shadow)

    patch_offset = (jj_len - jj_arm_ext) / np.sqrt(2)

    jj_patch_ref1 = jj_princeton_jj << jj_patches
    jj_patch_ref1.move((patch_offset, patch_offset + patch_len / 2 - patch_overlap))
    jj_patch_ref1.rotate(angle=135)
    jj_patch_ref2 = jj_princeton_jj << jj_patches
    jj_patch_ref2.move((patch_offset, -patch_offset - patch_len / 2 + patch_overlap))
    jj_patch_ref2.rotate(angle=135)

    jj_square_corner_x = square_offset_x - jj_arm2_wid / 2 + junction_arm_len_x
    jj_square_corner_y = square_offset_y + jj_arm1_wid / 2 - junction_arm_len_y
    jj_square_right_x = jj_square_corner_x + square_size
    jj_square_bottom_y = jj_square_corner_y - square_size

    jj_clip_extent = jj_len + patch_len + square_size + 10
    jj_cross_clip_mask = gf.Component()
    jj_cross_clip_mask.add_polygon(
        [
            (-jj_clip_extent, -jj_clip_extent),
            (jj_square_corner_x, -jj_clip_extent),
            (jj_square_corner_x, jj_square_bottom_y),
            (jj_square_right_x, jj_square_bottom_y),
            (jj_square_right_x, jj_square_corner_y),
            (jj_clip_extent, jj_square_corner_y),
            (jj_clip_extent, jj_clip_extent),
            (-jj_clip_extent, jj_clip_extent),
        ],
        layer=layer_jj,
    )
    jj_cross_clip_mask_ref = jj_princeton_jj << jj_cross_clip_mask
    jj_cross_clipped = gf.boolean(
        jj_cross_ref,
        jj_cross_clip_mask_ref,
        operation="and",
        layer=layer_jj,
    )

    if merge_jj_and_patches:
        jj_patches_for_merge = gf.Component()
        jj_patch_merge_ref1 = jj_patches_for_merge << jj_patches
        jj_patch_merge_ref1.move((patch_offset, patch_offset + patch_len / 2 - patch_overlap))
        jj_patch_merge_ref1.rotate(angle=135)
        jj_patch_merge_ref2 = jj_patches_for_merge << jj_patches
        jj_patch_merge_ref2.move((patch_offset, -patch_offset - patch_len / 2 + patch_overlap))
        jj_patch_merge_ref2.rotate(angle=135)
        jj_cross_patch_merge = gf.boolean(
            jj_cross_clipped,
            jj_patches_for_merge,
            operation="or",
            layer=layer_jj,
        )
        jj_princeton_jj = jj_cross_patch_merge
    else:
        jj_cross_and_patches = gf.Component()
        jj_cross_and_patches << jj_cross_clipped
        jj_patch_body_ref1 = jj_cross_and_patches << jj_patches
        jj_patch_body_ref1.move((patch_offset, patch_offset + patch_len / 2 - patch_overlap))
        jj_patch_body_ref1.rotate(angle=135)
        jj_patch_body_ref2 = jj_cross_and_patches << jj_patches
        jj_patch_body_ref2.move((patch_offset, -patch_offset - patch_len / 2 + patch_overlap))
        jj_patch_body_ref2.rotate(angle=135)
        jj_princeton_jj = jj_cross_and_patches

    jj_patches_shadow_ref1 = jj_princeton_shadow << jj_patches_shadow
    jj_patches_shadow_ref1.move((patch_offset, patch_offset + patch_len / 2 - patch_overlap))
    jj_patches_shadow_ref1.rotate(angle=135)
    jj_patches_shadow_ref2 = jj_princeton_shadow << jj_patches_shadow
    jj_patches_shadow_ref2.move((patch_offset, -patch_offset - patch_len / 2 + patch_overlap))
    jj_patches_shadow_ref2.rotate(angle=135)

    jj_princeton_jj_ref = jj_princeton << jj_princeton_jj
    jj_princeton << jj_princeton_shadow

    jj_square_center_x = jj_square_corner_x + square_size / 2
    jj_square_center_y = jj_square_corner_y - square_size / 2

    jj_square_ref = jj_princeton << gf.components.rectangle(
        size=(square_size, square_size),
        centered=True,
        layer=layer_jj,
    )
    jj_square_ref.move((jj_square_center_x, jj_square_center_y))

    if merge_jj_and_patches:
        jj_princeton_merge = gf.boolean(
            jj_princeton_jj_ref,
            jj_square_ref,
            operation="or",
            layer=layer_jj,
        )
        jj_princeton = gf.Component()
        jj_princeton << jj_princeton_shadow
        jj_princeton << jj_princeton_merge

    _ = (
        jj_shadow_len,
        jj_arm_shadow_overlap,
        layer_jj_shadow,
        pad_connection_overlap,
        square_connection_overlap,
    )

    oriented_jj = gf.Component()
    jj_ref = oriented_jj << jj_princeton
    jj_ref.rotate(angle=PRINCETON_JJ_INITIAL_ROTATION)
    oriented_jj.flatten()

    jj_princeton = oriented_jj

    return jj_princeton
