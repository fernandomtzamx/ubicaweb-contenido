<?php
/**
 * Plugin Name: UbicaWeb: redirecciones 301
 * Description: Redirige URLs viejas a su nuevo destino. La lista vive en el ajuste "ubicaweb_redirecciones" (JSON {"/ruta-vieja/": "/ruta-nueva/"}), que el pipeline del repo ubicaweb-contenido actualiza por la API REST. Sin plugins de terceros.
 * Version: 1.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Ajuste editable por la API REST (/wp/v2/settings), solo para administradores.
add_action(
	'init',
	function () {
		register_setting(
			'general',
			'ubicaweb_redirecciones',
			array(
				'type'         => 'string',
				'default'      => '{}',
				'show_in_rest' => true,
				'description'  => 'Redirecciones 301 en JSON: {"/ruta-vieja/": "/ruta-nueva/"}',
			)
		);
	}
);

add_action(
	'template_redirect',
	function () {
		$mapa = json_decode( (string) get_option( 'ubicaweb_redirecciones', '{}' ), true );
		if ( empty( $mapa ) || ! is_array( $mapa ) ) {
			return;
		}
		$ruta = wp_parse_url( isset( $_SERVER['REQUEST_URI'] ) ? (string) $_SERVER['REQUEST_URI'] : '/', PHP_URL_PATH );
		$ruta = '/' . trim( (string) $ruta, '/' ) . '/';
		if ( '//' === $ruta ) {
			$ruta = '/';
		}
		if ( isset( $mapa[ $ruta ] ) && is_string( $mapa[ $ruta ] ) && $mapa[ $ruta ] !== $ruta ) {
			wp_safe_redirect( home_url( $mapa[ $ruta ] ), 301, 'UbicaWeb' );
			exit;
		}
	},
	1
);
