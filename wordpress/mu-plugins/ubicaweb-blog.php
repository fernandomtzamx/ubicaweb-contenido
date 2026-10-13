<?php
/**
 * Plugin Name: UbicaWeb: listado del blog
 * Description: El listado de /blog/ (plantilla de entradas del tema) muestra solo artículos: deja fuera los términos del diccionario de SEO local y las entradas sin categoría (demo del tema). Las entradas siguen existiendo y abriendo en su URL.
 * Version: 1.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action(
	'pre_get_posts',
	function ( $query ) {
		if ( is_admin() || ! $query->is_main_query() || ! $query->is_home() ) {
			return;
		}
		$excluir = array();
		foreach ( array( 'diccionario-seo-local', 'uncategorized' ) as $slug ) {
			$cat = get_category_by_slug( $slug );
			if ( $cat ) {
				$excluir[] = (int) $cat->term_id;
			}
		}
		if ( $excluir ) {
			$query->set( 'category__not_in', $excluir );
		}
	}
);
