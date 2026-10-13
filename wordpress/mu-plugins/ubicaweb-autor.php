<?php
/**
 * Plugin Name: UbicaWeb: perfil de autor
 * Description: Dos versiones de la biografía del autor. La caja al pie de cada artículo usa la biografía corta (campo Información biográfica del usuario). La página de autor muestra la biografía larga (meta ubicaweb_bio_larga, editable por la API REST). La meta descripción de la página de autor se mantiene corta y el schema Person recibe descripción y temas de especialidad.
 * Version: 1.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Meta de usuario para la biografía larga, editable por la API (users/me).
add_action(
	'init',
	function () {
		register_meta(
			'user',
			'ubicaweb_bio_larga',
			array(
				'type'          => 'string',
				'single'        => true,
				'show_in_rest'  => true,
				'auth_callback' => function ( $allowed, $meta_key, $user_id ) {
					return current_user_can( 'edit_user', $user_id );
				},
			)
		);
	}
);

// En la página de autor, la biografía visible es la larga.
add_filter(
	'get_the_author_description',
	function ( $value, $user_id ) {
		if ( is_admin() || ! is_author() || doing_filter( 'aioseo_description' ) ) {
			return $value;
		}
		$larga = get_user_meta( (int) $user_id, 'ubicaweb_bio_larga', true );
		return $larga ? $larga : $value;
	},
	10,
	2
);

// Meta descripción de la página de autor: la biografía corta (cabe en el resultado de Google).
add_filter(
	'aioseo_description',
	function ( $description ) {
		if ( ! is_author() ) {
			return $description;
		}
		$autor = get_queried_object();
		if ( $autor instanceof WP_User ) {
			$corta = get_user_meta( $autor->ID, 'description', true );
			if ( $corta ) {
				return wp_strip_all_tags( $corta );
			}
		}
		return $description;
	}
);

// Schema Person: descripción y temas de especialidad.
add_filter(
	'aioseo_schema_output',
	function ( $graphs ) {
		if ( ! is_array( $graphs ) ) {
			return $graphs;
		}
		foreach ( $graphs as $i => $graph ) {
			if ( ! is_array( $graph ) || ( $graph['@type'] ?? '' ) !== 'Person' ) {
				continue;
			}
			$user = get_user_by( 'slug', basename( untrailingslashit( (string) ( $graph['url'] ?? '' ) ) ) );
			if ( ! $user ) {
				continue;
			}
			$corta = get_user_meta( $user->ID, 'description', true );
			if ( $corta ) {
				$graphs[ $i ]['description'] = wp_strip_all_tags( $corta );
			}
			$graphs[ $i ]['knowsAbout'] = array( 'SEO local', 'Sitios web', 'MarTech', 'Publicidad digital', 'Franquicias' );
			$same = get_user_meta( $user->ID, 'ubicaweb_same_as', true );
			if ( $same ) {
				$graphs[ $i ]['sameAs'] = array_values( array_filter( array_map( 'trim', explode( ',', $same ) ) ) );
			}
		}
		return $graphs;
	}
);

add_action(
	'init',
	function () {
		register_meta(
			'user',
			'ubicaweb_same_as',
			array(
				'type'          => 'string',
				'single'        => true,
				'show_in_rest'  => true,
				'auth_callback' => function ( $allowed, $meta_key, $user_id ) {
					return current_user_can( 'edit_user', $user_id );
				},
			)
		);
	}
);
